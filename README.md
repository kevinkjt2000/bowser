[![Build Status](https://img.shields.io/travis/kevinkjt2000/bowser/master.svg?label=Travis-CI)](https://travis-ci.org/kevinkjt2000/bowser?branch=master)
[![Coverage Status](https://img.shields.io/codecov/c/github/kevinkjt2000/bowser/master.svg?label=Codecov)](https://codecov.io/gh/kevinkjt2000/bowser/branch/master)
[![Dependency Status](https://pyup.io/repos/github/kevinkjt2000/bowser/shield.svg)](https://pyup.io/repos/github/kevinkjt2000/bowser)

[![Discord Bots](https://discordbots.org/api/widget/status/392875945717137418.svg)](https://discordbots.org/bot/392875945717137418)
[![Discord Bots](https://discordbots.org/api/widget/upvotes/392875945717137418.svg)](https://discordbots.org/bot/392875945717137418)
[![Discord Bots](https://discordbots.org/api/widget/lib/392875945717137418.svg)](https://discordbots.org/bot/392875945717137418)
# Bowser Bot for Discord
Bowser responds to commands, such as `!status`, by querying channel's configured game server and responding with a message that shows who is online, how many mods are loaded, etc.

### Setup
1. The server owner navigates to this link https://discordapp.com/oauth2/authorize?client_id=392875945717137418&scope=bot&permissions=0 .
2. Bowser is given read and write permissions on any channels where bowser should respond to commands.

### Usage
Any channel bowser has read and write permissions for, bowser will respond to the command `!help`.  Configuration is currently limited to one minecraft server per discord channel, and the administrator role is able to configure it with `!set <host> <port>`.
