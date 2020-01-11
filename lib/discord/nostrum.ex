defmodule Bowser.Discord.Nostrum do
  @behaviour Bowser.Discord
  @moduledoc "Wrapper of nostrum library"

  @impl Bowser.Discord
  def send_message(channel_id, msg) do
    Nostrum.Api.create_message!(channel_id, msg)
  end
end
