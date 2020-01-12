defmodule Bowser.Database do
  @moduledoc "Contract/wrapper for integration against various databases"

  # TODO: make config object have defstruct or something to enforce fields
  @callback get_config(guild_id :: String.t(), channel_id :: integer) :: Map.t()
  @callback get_all_configs(guild_id :: String.t(), channel_id :: integer) :: [Map.t()]
  @callback set_config(guild_id :: String.t(), channel_id :: integer, config :: Map.t()) ::
              no_return()
  @callback delete_config(guild_id :: String.t(), channel_id :: integer) :: no_return()
  @callback delete_guild_config(guild_id :: String.t()) :: no_return()
end
