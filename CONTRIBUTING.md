The following environment variables must be present:
* BOT_TOKEN - discord bot secret token
* COOKIE - secret string that is used to protect the elixir backend
* REDIS_PORT - pick an available network port on your system

You must activate these environment variables each time you open a new terminal for developing:

```sh
export $(cat .env | xargs)
```

Spin up the required redis instance (or use your own):

```sh
docker-compose up -d redis
```

At this point you can develop with a local installation of Elixir and/or docker. Elixir does not have to be installed if docker-compose is used to develop bowser; however, faster cycle times are obtainable when running with the mix commands listed above.

The typical `mix` tasks will help with development:

```sh
mix deps.get
mix test
iex -S mix
```

or

```sh
docker-compose up -d --build bot
```
