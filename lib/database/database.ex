defmodule Bowser.Database do
  @moduledoc "Contract/wrapper for integration against various databases"

  @callback get_config(guild_id :: String.t(), channel_id :: integer) :: String.t()
  @callback set_config(guild_id :: String.t(), channel_id :: integer, config :: String.t()) ::
              no_return()
  @callback delete_config(guild_id :: String.t(), channel_id :: integer) :: no_return()
end
