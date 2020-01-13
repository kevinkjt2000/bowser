defmodule Bowser.Discord do
  @moduledoc "Contract/wrapper for integration against discord"

  @callback send_message(channel_id :: integer, msg :: String.t()) :: no_return()
  @callback get_guild_by_id(guild_id :: String.t()) :: Nostrum.Struct.Guild.t()
end
