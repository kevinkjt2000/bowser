import Config

config :bowser,
  redis_port: String.to_integer(System.fetch_env!("REDIS_PORT"))

config :nostrum,
  token: System.fetch_env!("BOT_TOKEN")
