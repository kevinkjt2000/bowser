defmodule BowserDatabaseRedixTest do
  use ExUnit.Case, async: true
  doctest Bowser.Database.Redix

  describe "get_config/2" do
    test "older servers without nicknames default to nil" do
      Bowser.Database.Redix.set_config("7890", 123_456, %{})
      assert config = Bowser.Database.Redix.get_config("7890", 123_456)
      assert Map.fetch!(config, "nickname") == nil
    end
  end
end
