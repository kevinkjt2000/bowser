[![Build Status](https://img.shields.io/travis/kevinkjt2000/bowser/master.svg?style=flat-square&label=Travis-CI)](https://travis-ci.org/kevinkjt2000/bowser?branch=master)
[![Coverage Status](https://img.shields.io/codecov/c/github/kevinkjt2000/bowser/master.svg?style=flat-square&label=Codecov)](https://codecov.io/gh/kevinkjt2000/bowser/branch/master/graph/badge.svg)
[![Dependency Status](https://img.shields.io/gemnasium/kevinkjt2000/bowser.svg)](https://beta.gemnasium.com/projects/github.com/kevinkjt2000/bowser)
# Bowser Bot for Discord
Adding this bot to a discord server will allow users to send the message "!status" to see current status about the minecraft server configured in `servers.json`.  Configuration is limited to one minecraft server per discord channel, but you can have a different server on each channel of your discord server if you like.  Eventually I will make my instance of this bot public and add commands that allow some discord role to be able to configure minecraft servers dynamically.  For now, feel free to run the bot, or ping me on discord.

### Preparation
* Create a `token.txt` file with your app bot user token from https://discordapp.com/developers/applications/me
* The server owner must add the bot by using the app client id in this link and browsing to it https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_NUMBER_HERE&scope=bot&permissions=0
* Give the bot read and write permissions for messages on any channels where you want the bot to respond
* Create a `servers.json` file (the IDs can be found by using [developer mode](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-))
```json
{
    "server_id1": {
        "channel_id1": { "host": "example.com", "port": 25565 },
        "channel_id2": { "host": "other.com", "port": 25565 }
    }
}
```
* Clone this repository or extract a downloaded zip copy

### Installation (without Docker)
* Ensure Python 3.6+ is installed
* Run `pip install -e .`
* Run the bot with `bowser-bot`

### Installation (with Docker)
* This was tested with Docker 17.12
* Run `docker-compose up -d` to start the services
* The logs can then be checked with `docker-compose logs -f`

### Usage
Any channel the bot has read and write permissions for, the bot will respond to the message `!help`
