defmodule Bowser.Redis.Mock do
  @moduledoc "Mock of redis implementation for unit tests"

  def command!(_conn, ["HGET" | args]) do
    case args do
      ["dm", _channel_id] ->
        "{\"host\":\"localhost\",\"port\":20000}"
      ["7890", 123_456] ->
        "{\"host\":\"localhost\",\"port\":20000}"
    end
  end
end
