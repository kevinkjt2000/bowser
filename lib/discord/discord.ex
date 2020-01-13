defmodule Bowser.Discord do
  @moduledoc "Contract/wrapper for integration against discord"

  @callback send_message(channel_id :: integer, msg :: String.t()) :: no_return()
  @callback get_guild_by_id(guild_id :: String.t()) :: Nostrum.Struct.Guild.t()
  @callback get_permissions_of_member(
              member :: Nostrum.Struct.Guild.Member,
              guild :: Nostrum.Struct.Guild.t(),
              channel_id :: integer
            ) :: [Nostrum.Permission.t()]
end
