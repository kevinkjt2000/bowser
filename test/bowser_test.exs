defmodule BowserTest do
  use ExUnit.Case, async: true
  doctest Bowser

  defmodule MockDiscord do
    @behaviour Bowser.Discord
    @moduledoc "Stub for mocking out discord API"

    @impl Bowser.Discord
    def send_message(channel_id, msg) do
      send(self(), {channel_id, msg})
    end

    @impl Bowser.Discord
    def get_guild_by_id(guild_id) do
      :ets.lookup(:mock_discord_guilds, guild_id)
      |> Enum.at(0)
      |> elem(1)
    end

    @impl Bowser.Discord
    def get_permissions_of_member(member, guild, channel_id) do
      Nostrum.Struct.Guild.Member.guild_channel_permissions(member, guild, channel_id)
    end
  end

  setup_all do
    :ets.new(:mock_discord_guilds, [:set, :named_table, :public, read_concurrency: true])
    Application.put_env(:bowser, :discord_impl, MockDiscord)
    :ok
  end

  setup do
    guild_id = System.unique_integer([:monotonic, :positive]) |> Integer.to_string()
    channel_id = System.unique_integer([:monotonic, :positive])

    administrator_role_id = System.unique_integer([:monotonic, :positive])

    administrator_role = %Nostrum.Struct.Guild.Role{
      id: administrator_role_id,
      permissions: Nostrum.Permission.to_bit(:administrator)
    }

    admin_id = System.unique_integer([:monotonic, :positive])

    admin = %Nostrum.Struct.User{
      id: admin_id
    }

    guild = %Nostrum.Struct.Guild{
      id: guild_id,
      members: %{
        admin_id => %Nostrum.Struct.Guild.Member{
          user: admin,
          roles: [administrator_role_id]
        }
      },
      roles: %{
        administrator_role_id => administrator_role
      },
      channels: %{
        channel_id => %Nostrum.Struct.Channel{
          id: channel_id,
          permission_overwrites: []
        }
      }
    }

    :ets.insert(:mock_discord_guilds, {guild_id, guild})

    [
      guild_id: guild_id,
      channel_id: channel_id,
      admin: admin
    ]
  end

  describe "ip_command/1" do
    test "sends a message containing the host and port configured for the channel", %{
      guild_id: guild_id,
      channel_id: channel_id
    } do
      host = "localhost"
      port = 20_000
      Bowser.Database.Redix.set_config(guild_id, channel_id, %{"host" => host, "port" => port})
      msg = %Nostrum.Struct.Message{guild_id: guild_id, channel_id: channel_id}
      Bowser.ip_command(msg)

      expected_response = {channel_id, "`#{host}:#{port}`"}
      assert_received(^expected_response)
    end
  end

  describe "set_command/3" do
    test "nicknames persist when setting configuration", %{
      guild_id: guild_id,
      channel_id: channel_id,
      admin: admin
    } do
      config = %{
        "host" => "localhost",
        "port" => 20_000,
        "nickname" => "jolly"
      }

      Bowser.Database.Redix.set_config(guild_id, channel_id, config)

      set_msg = %Nostrum.Struct.Message{
        guild_id: guild_id,
        channel_id: channel_id,
        content: "!set #{config["host"]} #{config["port"]} #{config["nickname"]}",
        author: admin
      }

      Bowser.handle_event({:MESSAGE_CREATE, set_msg, nil})

      expected_set_response =
        {channel_id, "Added `#{config["host"]}:#{config["port"]}` to the database."}

      assert_received(^expected_set_response)

      statuses_msg = %Nostrum.Struct.Message{
        guild_id: guild_id,
        channel_id: channel_id,
        content: "!statuses",
        author: admin
      }

      Bowser.handle_event({:MESSAGE_CREATE, statuses_msg, nil})

      # TODO: ponder if the nickname should be part of the error message
      # TODO: mock out the minecraft protocol to assert nickname shows
      expected_statuses_response =
        {channel_id, "`#{config["host"]}` refused the connection to port #{config["port"]}."}

      assert_received(^expected_statuses_response)
    end
  end
end
