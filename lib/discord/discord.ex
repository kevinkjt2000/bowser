defmodule Bowser.Discord do
  @moduledoc "Contract/wrapper for integration against discord"

  @callback send_message(channel_id :: integer, msg :: String.t()) :: no_return()
end
