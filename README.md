[![Build Status](https://img.shields.io/travis/kevinkjt2000/bowser/master.svg?style=flat-square&label=Travis-CI)](https://travis-ci.org/kevinkjt2000/bowser?branch=master)
[![Coverage Status](https://img.shields.io/codecov/c/github/kevinkjt2000/bowser/master.svg?style=flat-square&label=Codecov)](https://codecov.io/gh/kevinkjt2000/bowser/branch/master)
[![Dependency Status](https://pyup.io/repos/github/kevinkjt2000/bowser/shield.svg)](https://pyup.io/repos/github/kevinkjt2000/bowser)
# Bowser Bot for Discord
Adding this bot to a discord server will allow users to send commands like `!status` to see current status about the minecraft server configured for the channel.

### Setup
* The server owner may add the bot by using this link https://discordapp.com/oauth2/authorize?client_id=392875945717137418&scope=bot&permissions=0 .
* Give the bot read and write permissions for messages on any channels where you want the bot to respond to commands.

### Usage
Any channel the bot has read and write permissions for, the bot will respond to the command `!help`.  Configuration is currently limited to one minecraft server per discord channel, and the administrator role is able to configure it with `!set <host> <port>`.
