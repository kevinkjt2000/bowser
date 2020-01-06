defmodule Bowser.Redis do
  @moduledoc "I don't care about docs yet"
  @redis Application.get_env(:bowser, :redis_impl)

  def get_guild_channel_config(guild_id, channel_id) do
    @redis.command!(:redix, ["HGET", guild_id, channel_id])
  end
end
