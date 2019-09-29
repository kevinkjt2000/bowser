defmodule Bowser.MixProject do
  use Mix.Project

  def project do
    [
      app: :bowser,
      version: "0.1.0",
      elixir: "~> 1.6",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: extra_applications(Mix.env()),
      mod: {Bowser.Application, []}
    ]
  end

  defp extra_applications(:dev), do: extra_applications(:all) ++ [:remix]
  defp extra_applications(_all), do: [:logger, :nostrum]

  defp deps do
    [
      {:credo, "~> 1.0.0", only: [:dev, :test], runtime: false},
      {:distillery, "~> 2.0", runtime: false},
      {:jason, "~> 1.1"},
      {:mcping, git: "https://github.com/kevinkjt2000/mcping-elixir.git"},
      {:nostrum, "~> 0.4"},
      {:redix, "~> 0.8"},
      {:remix, git: "https://github.com/harlantwood/remix.git", only: :dev}
    ]
  end
end
