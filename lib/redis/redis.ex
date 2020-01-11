defmodule Bowser.Redis do
  @moduledoc "I don't care about docs yet"

  def get_guild_channel_config(guild_id, channel_id) do
    redis_impl().command!(:redix, ["HGET", guild_id, channel_id])
  end

  defp redis_impl do
    Application.get_env(:bowser, :redis_impl)
  end
end
