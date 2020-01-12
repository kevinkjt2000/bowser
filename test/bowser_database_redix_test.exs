defmodule BowserDatabaseRedixTest do
  use ExUnit.Case, async: true
  doctest Bowser.Database.Redix

  @moduletag :integration_redix

  setup_all do
    redis_host = "localhost"
    redis_port = 6380
    {:ok, _} = Application.ensure_all_started(:redix)
    {:ok, _pid} = Redix.start_link([host: redis_host, port: redis_port, name: :redix])
    :ok
  end

  describe "get_config/2" do
    test "older servers without nicknames default to nil" do
      Bowser.Database.Redix.set_config("7890", 123_456, "{}")
      assert config = Bowser.Database.Redix.get_config("7890", 123_456)
      assert Map.fetch!(config, "nickname") == nil
    end
  end
end
