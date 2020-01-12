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
  end

  setup_all do
    Application.put_env(:bowser, :discord_impl, MockDiscord)
    :ok
  end

  setup do
    guild_id = System.unique_integer([:monotonic, :positive]) |> Integer.to_string()
    channel_id = System.unique_integer([:monotonic, :positive])

    [
      guild_id: guild_id,
      channel_id: channel_id
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
      msg = %{guild_id: guild_id, channel_id: channel_id}
      Bowser.ip_command(msg)

      expected_message = {channel_id, "`#{host}:#{port}`"}
      assert_received(^expected_message)
    end
  end
end
