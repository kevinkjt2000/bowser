[![Build Status](https://img.shields.io/travis/kevinkjt2000/discord-minecraft-server-status/master.svg?style=flat-square&label=Travis-CI)](https://travis-ci.org/kevinkjt2000/discord-minecraft-server-status) [![Coverage Status](https://img.shields.io/coveralls/kevinkjt2000/discord-minecraft-server-status/master.svg?style=flat-square&label=Coveralls)](https://coveralls.io/github/kevinkjt2000/discord-minecraft-server-status?branch=master)
# Minecraft Server Status Bot for Discord
Adding this bot to a discord server will allow users to send the message "!status" to see current status about the minecraft server configured in [src/Minecraft.py](src/Minecraft.py).  There are plans to make this more generic later by having the bot store configured servers to a file, but for now this is manually configured and limited to one minecraft server per running instance of this bot.  Eventually I will make my instance of this bot public so that any server can use it when the bot can store configurations on a per discord server basis.

### Usage
* Ensure Python 3.6+ is installed
* Clone this repository or extract a downloaded zip copy
* Run `pip install -U -r requirements.txt`
* Create a file "token.txt" with your app bot user token from https://discordapp.com/developers/applications/me
* Run the bot with `python src/main.py`
* Have the server owner add the bot by using your app client id in this link https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_NUMBER_HERE&scope=bot&permissions=0
* Give the bot read and write permissions for messages on any channels where you want the bot to respond
