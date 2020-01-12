redis_host = Application.fetch_env!(:bowser, :redis_host)
redis_port = Application.fetch_env!(:bowser, :redis_port)
{:ok, _} = Application.ensure_all_started(:redix)
{:ok, _} = Redix.start_link(name: :redix, host: redis_host, port: redis_port)

ExUnit.start()
