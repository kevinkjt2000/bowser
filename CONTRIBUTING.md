The typical `mix` tasks will help with development:
```sh
mix deps.get
mix test
iex -S mix
```

Elixir does not have to be installed if docker-compose is used to develop bowser; however, faster cycle times are obtainable when running with the mix commands listed above.  A redis database is required, and a docker-compose configuration is provided to simplify running a redis database.

The following environment variables must be present:
* BOT_TOKEN - discord bot secret token
* COOKIE - secret string that is used to protect the elixir backend
