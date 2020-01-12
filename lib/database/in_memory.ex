defmodule Bowser.Database.InMemory do
  @moduledoc "Mock of Database implementation for unit tests"
  @behaviour Bowser.Database

  @impl Bowser.Database
  def get_config("dm", _channel_id) do
    %{"host" => "localhost", "port" => 20_000}
  end

  def get_config("7890", 123_456) do
    %{"host" => "localhost", "port" => 20_000}
  end

  @impl Bowser.Database
  def get_all_configs(_guild_id, _channel_id) do
    []
  end

  @impl Bowser.Database
  def delete_config(_guild_id, _channel_id) do
  end

  @impl Bowser.Database
  def set_config(_guild_id, _channel_id, _config) do
  end
end
