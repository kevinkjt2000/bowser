defmodule Bowser.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application
  use Supervisor

  def start_link do
    Supervisor.start_link(__MODULE__, :ok)
  end

  def start(_type, _args) do
    {redis_port, ""} = Integer.parse(Application.get_env(:bowser, :redis_port))

    children = [
      worker(Bowser, []),
      {Redix, name: :redix, host: Application.get_env(:bowser, :redis_host), port: redis_port}
    ]

    Process.flag(:trap_exit, true)
    Supervisor.start_link(children, strategy: :one_for_one)
  end

  def init(:ok) do
    __MODULE__.start_link()
  end
end
