defmodule Bowser.Discord.Mock do
  @behaviour Bowser.Discord
  @moduledoc "Stub for mocking out discord API"

  @impl Bowser.Discord
  def send_message(_, _) do
  end
end
