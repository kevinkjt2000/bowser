use Mix.Config

if Mix.env() == :dev do
  config :remix,
    escript: false,
    silent: true

  config :nostrum,
    token: System.get_env("BOT_TOKEN")

  config :bowser,
    redis_host: "localhost"
end

if Mix.env() == :prod do
  config :bowser,
    redis_host: "redis"
end
