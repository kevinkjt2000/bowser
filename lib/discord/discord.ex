defmodule Bowser.Discord do
  @moduledoc "Contract/wrapper for integration against discord"
  @discord Application.get_env(:bowser, :discord_impl)

  def send_message(channel_id, msg) do
    @discord.send_message(channel_id, msg)
  end
end
