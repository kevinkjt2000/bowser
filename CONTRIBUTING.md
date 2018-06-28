So you want to hack on bowser?  Well, you have come to the right place for learning how to run and test bowser (IDE configuration is up to you; just be sure to use editor-config).

You will need to setup a `.env` that contains tokens (`BOWSER_TOKEN` and `KOOPA_TOKEN`) only if you plan to run a real instance of the bot.  Travis CI handles running the real bot as part of integration testing, so you may find that unit tests are sufficient (and they do not require any tokens to run).

The eventual goal is to dockerize all the needed development tools, and launch all dev tasks from a Makefile.  Unfortunately, `pipenv` is not yet one of the dockerized tools, so you will need to install that first.  Without further ado, here are things you will likely want to do:

```sh
pip install --user pipenv  # ensure that ~/.local/bin is in your PATH
make test  # unit tests
make run  # to run a development version
make tests-integration  # restarts/runs the development version and uses another bot to test the development bot
```
