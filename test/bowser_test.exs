defmodule BowserTest do
  use ExUnit.Case, async: true
  doctest Bowser

  describe "ip_command/1" do
    test "sends a message containing the host and port configured for the channel" do
      msg = %{guild_id: "7890", channel_id: 123_456}
      Bowser.ip_command(msg)

      assert "create_message was called with ?"
    end
  end

  describe "get_guild_channel_config/2" do
    test "older servers without nicknames default to nil" do
    end
  end
end
