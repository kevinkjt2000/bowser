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
  end

  describe "ip_command/1" do
    test "sends a message containing the host and port configured for the channel" do
      msg = %{guild_id: "7890", channel_id: 123_456}
      Bowser.ip_command(msg)

      assert_received({123_456, "`localhost:20000`"})
    end
  end
end
