defmodule Bowser.Database.Redix do
  @behaviour Bowser.Database
  @moduledoc "Wrapper of redix library"

  @impl Bowser.Database
  def get_config(guild_id, channel_id) do
    Redix.command!(:redix, ["HGET", guild_id, channel_id])
  end

  @impl Bowser.Database
  def set_config(guild_id, channel_id, config) do
    Redix.command!(:redix, [
      "HSET",
      guild_id,
      channel_id,
      config
    ])
  end

  @impl Bowser.Database
  def delete_config(guild_id, channel_id) do
    Redix.command!(:redix, ["HDEL", guild_id, channel_id])
  end
end
