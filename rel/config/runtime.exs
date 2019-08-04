use Mix.Config

config :nostrum,
  token: System.get_env("BOT_TOKEN")

config :bowser,
  redis_port: System.get_env("REDIS_PORT")
