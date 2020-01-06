defmodule Bowser.Discord.Nostrum do
  @moduledoc "Wrapper of nostrum library"

  def send_message(channel_id, msg) do
    Nostrum.Api.create_message!(channel_id, msg)
  end
end
