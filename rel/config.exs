# Import all plugins from `rel/plugins`
# They can then be used by adding `plugin MyPlugin` to
# either an environment, or release definition, where
# `MyPlugin` is the name of the plugin module.
~w(rel plugins *.exs)
|> Path.join()
|> Path.wildcard()
|> Enum.map(&Code.eval_file(&1))

use Mix.Releases.Config,
  # This sets the default release built by `mix release`
  default_release: :default,
  # This sets the default environment used by `mix release`
  default_environment: Mix.env()

# For a full list of config options for both releases
# and environments, visit https://hexdocs.pm/distillery/config/distillery.html

environment :dev do
  set(dev_mode: true)
  set(include_erts: false)

  set(cookie: :crypto.hash(:sha256, ":testing") |> Base.encode16() |> String.to_atom())
end

environment :prod do
  set(
    config_providers: [
      {
        Mix.Releases.Config.Providers.Elixir,
        ["${RELEASE_ROOT_DIR}/etc/runtime.exs"]
      }
    ],
    overlays: [
      {:copy, "rel/config/runtime.exs", "etc/runtime.exs"}
    ]
  )

  set(include_erts: true)
  set(include_src: false)

  set(
    cookie: :crypto.hash(:sha256, System.get_env("COOKIE")) |> Base.encode16() |> String.to_atom()
  )

  set(vm_args: "rel/vm.args")
end

release :bowser do
  set(version: current_version(:bowser))

  set(
    applications: [
      :runtime_tools
    ]
  )
end
