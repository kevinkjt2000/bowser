use Mix.Config

if Mix.env() == :dev do
  # Even though production also uses REDIS_PORT and BOT_TOKEN,
  # those variables must be given via runtime configuration instead.
  # (see: rel/config/runtime.exs)
  config :bowser,
    redis_host: "localhost",
    redis_port: System.get_env("REDIS_PORT")

  config :nostrum,
    token: System.get_env("BOT_TOKEN")

  config :remix,
    escript: false,
    silent: true
end

if Mix.env() == :prod do
  config :bowser,
    redis_host: "redis"
end
