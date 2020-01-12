defmodule Bowser.Database.Redix do
  @behaviour Bowser.Database
  @moduledoc "Wrapper of redix library"

  alias Protocols.ProtocolError

  @impl Bowser.Database
  def get_config(guild_id, channel_id) do
    json = Redix.command!(:redix, ["HGET", guild_id, channel_id])
    if json do
      Jason.decode!(json)
      |> Map.put_new("nickname", nil)
    else
      raise ProtocolError, message: "There is not yet a game server configured for this channel."
    end
  end

  @impl Bowser.Database
  def get_all_configs(guild_id, _channel_id) do
    Redix.command!(:redix, ["HVALS", guild_id])
    |> Enum.map(fn data ->
      data
      |> Map.put_new("nickname", nil)
    end)
  end

  @impl Bowser.Database
  def set_config(guild_id, channel_id, config) do
    Redix.command!(:redix, [
      "HSET",
      guild_id,
      channel_id,
      Jason.encode!(config)
    ])
  end

  @impl Bowser.Database
  def delete_config(guild_id, channel_id) do
    Redix.command!(:redix, ["HDEL", guild_id, channel_id])
  end
end
