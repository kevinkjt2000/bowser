defmodule Bowser do
  @moduledoc "Discord command handler"

  use Nostrum.Consumer
  require Logger

  alias Protocols.ProtocolError

  @doc """
  Returns the IP and port of the configured server.
  """
  def ip_command(msg) do
    %{"host" => host, "port" => port} = get_game_server_info!(msg)
    discord_impl().send_message(msg.channel_id, "`#{host}:#{port}`")
  end

  @doc """
  Returns the version of the "forge" mod, if it is installed on the server.
  """
  def forge_command(msg) do
    %{"host" => host, "port" => port} = get_game_server_info!(msg)
    forge = Protocols.Minecraft.get_forge_version(host, port)
    discord_impl().send_message(msg.channel_id, forge)
  end

  @doc """
  Displays the server's message of the day (MOTD).
  """
  def motd_command(msg) do
    %{"host" => host, "port" => port} = get_game_server_info!(msg)
    motd = Protocols.Minecraft.get_motd(host, port)
    discord_impl().send_message(msg.channel_id, motd)
  end

  @doc """
  Fetches the status from the server, shows online players, and shows the number of mods installed.
  """
  def status_command(msg) do
    %{"host" => host, "port" => port} = get_game_server_info!(msg)
    status = Protocols.Minecraft.get_status_message(host, port)
    discord_impl().send_message(msg.channel_id, status)
  end

  defp check_set_perms(msg) do
    case msg.guild_id do
      nil ->
        :noop

      _ ->
        guild = discord_impl().get_guild_by_id(msg.guild_id)
        member = Map.get(guild.members, msg.author.id)

        perms =
          Nostrum.Struct.Guild.Member.guild_channel_permissions(member, guild, msg.channel_id)

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
  end

  @doc """
  When given a host and port, that information will be stored to the database for the status command to use later. If the command is used by itself, the information stored for the channel that the command originated from is erased.
  Note: You must be assigned a role named "mario" or have at least one of the following permissions: manage channels, manage guild, manage roles, or administrator.
  """
  def set_command(msg, []) do
    check_set_perms(msg)

    guild_id =
      case msg.guild_id do
        nil -> "dm"
        _ -> msg.guild_id
      end

    database_impl().delete_config(guild_id, msg.channel_id)

    discord_impl().send_message(
      msg.channel_id,
      "Server configuration has been removed from this channel."
    )
  end

  def set_command(msg, [host]) do
    set_command(msg, [host, "25565"])
  end

  def set_command(msg, [host, port]) do
    set_command(msg, [host, port, nil])
  end

  def set_command(msg, [host, port, nickname]) do
    check_set_perms(msg)
    {int_port, ""} = Integer.parse(port)

    guild_id =
      case msg.guild_id do
        nil -> "dm"
        _ -> msg.guild_id
      end

    database_impl().set_config(
      guild_id,
      msg.channel_id,
      %{"host" => host, "port" => int_port, "nickname" => nickname}
    )

    discord_impl().send_message(
      msg.channel_id,
      "Added `#{host}:#{port}` to the database."
    )
  end

  def set_command(msg, _wrong_args) do
    discord_impl().send_message(msg.channel_id, "Incorrect arguments given.")
  end

  @doc """
  Does the status command for every channel, aggregating the data into one message.
  """
  def statuses_command(msg) do
    datas =
      case msg.guild_id do
        nil ->
          [Redix.command!(:redix, ["HGET", "dm", msg.channel_id])]

        _ ->
          database_impl().get_all_configs(msg.guild_id, msg.channel_id)
      end

    statuses =
      for data <- datas do
        # TODO: parallelize this list comprehension
        %{"host" => host, "port" => port, "nickname" => nickname} = data

        try do
          status = Protocols.Minecraft.get_status_message(host, port)

          case nickname do
            nil -> "#{host} #{status}"
            _ -> "#{nickname} #{host} #{status}"
          end
        rescue
          err in ProtocolError -> err.message
        end
      end
      |> Enum.join("\n")

    discord_impl().send_message(
      msg.channel_id,
      case statuses do
        "" -> "Nothing has been configured yet."
        _ -> statuses
      end
    )
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

    discord_impl().send_message(
      msg.channel_id,
      "```#{helps}```\nJoin https://discord.gg/dXe38sa if you have questions about this bot."
    )
  end

  def handle_event({:READY, _thing, _ws_state}) do
    channels = Redix.command!(:redix, ["DBSIZE"])
    Logger.info("🎬 Bowser is ready, and currently serving #{channels} guild(s).")
  end

  def handle_event({:CHANNEL_DELETE, channel, _ws_state}) do
    database_impl().delete_config(channel.guild_id, channel.id)
  end

  def handle_event({:GUILD_DELETE, {guild, _unavailable}, _ws_state}) do
    database_impl().delete_guild_config(guild.id)
  end

  @command_prefix "!"
  def handle_event({:MESSAGE_CREATE, msg, _ws_state}) do
    [prefix_cmd | args] = String.split(msg.content, " ")

    try do
      case prefix_cmd do
        @command_prefix <> cmd ->
          cond do
            cmd in ["help", "ip", "forge", "motd", "status", "statuses"] ->
              :erlang.apply(__MODULE__, String.to_atom(cmd <> "_command"), [msg])

            cmd in ["set"] ->
              :erlang.apply(__MODULE__, String.to_atom(cmd <> "_command"), [msg, args])

            true ->
              :ignore
          end

        _ ->
          :ignore
      end
    rescue
      err in ProtocolError ->
        discord_impl().send_message(msg.channel_id, err.message)

      err ->
        Logger.error(Exception.format(:error, err, __STACKTRACE__))

        discord_impl().send_message(
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

  defp get_game_server_info!(msg) do
    guild_id =
      case msg.guild_id do
        nil -> "dm"
        _ -> msg.guild_id
      end

    database_impl().get_config(guild_id, msg.channel_id)
  end

  defp discord_impl do
    Application.get_env(:bowser, :discord_impl)
  end

  defp database_impl do
    Application.get_env(:bowser, :database_impl)
  end
end
