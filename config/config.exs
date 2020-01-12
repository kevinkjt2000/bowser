import Config

config :bowser,
  discord_impl: Bowser.Discord.Nostrum,
  database_impl: Bowser.Database.Redix

if Mix.env() == :dev do
  # Even though production also uses REDIS_PORT and BOT_TOKEN,
  # those variables must be given via runtime configuration instead.
  # (see: config/releases.exs)
  config :bowser,
    redis_host: "localhost",
    redis_port: String.to_integer(System.fetch_env!("REDIS_PORT"))

  config :nostrum,
    token: System.fetch_env!("BOT_TOKEN")

  config :remix,
    escript: false,
    silent: true
end

if Mix.env() == :test do
  config :bowser,
    redis_host: "localhost",
    redis_port: String.to_integer(System.fetch_env!("REDIS_PORT"))
end

if Mix.env() == :prod do
  config :bowser,
    redis_host: "redis"
end
