defmodule Bowser do
  use Nostrum.Consumer

  alias Nostrum.Api
  alias Protocols.ProtocolError

  @doc """
  Returns the IP and port of the configured server.
  """
  def ip_command(msg) do
    %{"host" => host, "port" => port} = _get_game_server_info!(msg)
    Api.create_message(msg.channel_id, "`#{host}:#{port}`")
  end

  @doc """
  Returns the version of the "forge" mod, if it is installed on the server.
  """
  def forge_command(msg) do
    %{"host" => host, "port" => port} = _get_game_server_info!(msg)
    forge = Protocols.Minecraft.get_forge_version(host, port)
    Api.create_message!(msg.channel_id, forge)
  end

  @doc """
  Displays the server's message of the day (MOTD).
  """
  def motd_command(msg) do
    %{"host" => host, "port" => port} = _get_game_server_info!(msg)
    motd = Protocols.Minecraft.get_motd(host, port)
    Api.create_message!(msg.channel_id, motd)
  end

  @doc """
  Fetches the status from the server, shows online players, and shows the number of mods installed.
  """
  def status_command(msg) do
    %{"host" => host, "port" => port} = _get_game_server_info!(msg)
    status = Protocols.Minecraft.get_status_message(host, port)
    Api.create_message!(msg.channel_id, status)
  end

  def _check_set_perms(msg) do
    guild = Nostrum.Cache.GuildCache.get!(msg.guild_id)
    member = Map.get(guild.members, msg.author.id)

    perms = Nostrum.Struct.Guild.Member.guild_channel_permissions(member, guild, msg.channel_id)

    if Enum.all?(
         [:administrator, :manage_channels, :manage_guild, :manage_roles],
         &(&1 not in perms)
       ) do
      mario_roles =
        guild.roles
        |> Enum.filter(fn {_id, %{name: name}} -> name == "mario" end)
        |> Enum.map(fn {id, _role} -> id end)

      if Enum.all?(member.roles, &(&1 not in mario_roles)) do
        raise ProtocolError, message: "You do not have permission to use this command."
      end
    end
  end

  @doc """
  When given a host and port, that information will be stored to the database for the status command to use later.
  If the command is used by itself, the information stored for the channel that the command originated from is erased.
  """
  def set_command(msg, []) do
    _check_set_perms(msg)

    Redix.command!(:redix, ["HDEL", msg.guild_id, msg.channel_id])

    Api.create_message!(
      msg.channel_id,
      "Server configuration has been removed from this channel."
    )
  end

  def set_command(msg, [host]) do
    set_command(msg, [host, "25_565"])
  end

  def set_command(msg, [host, port]) do
    # TODO: validate user input

    _check_set_perms(msg)
    {int_port, ""} = Integer.parse(port)

    Redix.command!(:redix, [
      "HSET",
      msg.guild_id,
      msg.channel_id,
      Jason.encode!(%{"host" => host, "port" => int_port})
    ])

    Api.create_message!(
      msg.channel_id,
      "Added `#{host}:#{port}` to the database."
    )
  end

  def set_command(msg, _wrong_args) do
    Api.create_message!(msg.channel_id, "Incorrect arguments given.")
  end

  @doc """
  Does the status command for every channel, aggregating the data into one message.
  """
  def statuses_command(msg) do
    datas = Redix.command!(:redix, ["HVALS", msg.guild_id])

    statuses =
      for data <- datas do
        # TODO: parallelize this list comprehension
        %{"host" => host, "port" => str_port} = Jason.decode!(data)
        {port, ""} = Integer.parse(str_port)

        try do
          status = Protocols.Minecraft.get_status_message(host, port)
          "#{host} #{status}"
        rescue
          err in ProtocolError -> err.message
        end
      end
      |> Enum.join("\n")

    Api.create_message!(msg.channel_id, statuses)
  end

  @doc """
  Prints information about each command.
  """
  def help_command(msg) do
    {:docs_v1, _, :elixir, _, _, _, docs} = Code.fetch_docs(Bowser)

    helps =
      for {{:function, func, _}, _, _, %{"en" => doc}, _} <- docs do
        command = func |> to_string |> String.replace_suffix("_command", "")
        "!#{command} - #{doc}"
      end
      |> Enum.join("\n")

    Api.create_message!(msg.channel_id, "```#{helps}```")
  end

  def handle_event({:GUILD_DELETE, {guild, _unavailable}, _ws_state}) do
    Redix.command!(:redix, ["DEL", guild.id])
  end

  def handle_event({:CHANNEL_DELETE, {channel}, _ws_state}) do
    Redix.command!(:redix, ["HDEL", channel.guild_id, channel.id])
  end

  def handle_event({:MESSAGE_CREATE, {msg}, _ws_state}) do
    [cmd | args] = String.split(msg.content, " ")

    try do
      case cmd do
        "!help" -> help_command(msg)
        "!ip" -> ip_command(msg)
        "!forge" -> forge_command(msg)
        "!motd" -> motd_command(msg)
        "!set" -> set_command(msg, args)
        "!status" -> status_command(msg)
        "!statuses" -> statuses_command(msg)
        _ -> :ignore
      end
    rescue
      err in ProtocolError ->
        Api.create_message!(msg.channel_id, err.message)

      err ->
        IO.inspect(__STACKTRACE__)
        IO.inspect(err)

        Api.create_message!(
          msg.channel_id,
          "Ninjas hijacked the packets, but the bot author will probably fix it."
        )
    end
  end

  def handle_event(_event) do
    :noop
  end

  def start_link do
    Consumer.start_link(__MODULE__)
  end

  def _get_game_server_info!(msg) do
    json = Redix.command!(:redix, ["HGET", msg.guild_id, msg.channel_id])

    if json do
      Jason.decode!(json)
    else
      raise ProtocolError, message: "There is not yet a game server configured for this channel."
    end
  end
end
