[![Build Status](https://img.shields.io/travis/kevinkjt2000/bowser/master.svg?label=Travis-CI)](https://travis-ci.org/kevinkjt2000/bowser?branch=master)
[![Discord Chat](https://img.shields.io/discord/339549920338116611.svg)](https://discord.gg/dXe38sa)

[![Discord Bots](https://discordbots.org/api/widget/status/392875945717137418.svg)](https://discordbots.org/bot/392875945717137418)
[![Discord Bots](https://discordbots.org/api/widget/upvotes/392875945717137418.svg)](https://discordbots.org/bot/392875945717137418)
[![Discord Bots](https://discordbots.org/api/widget/lib/392875945717137418.svg)](https://discordbots.org/bot/392875945717137418)
# Bowser Bot for Discord
Bowser responds to commands, such as `!status`, by querying channel's configured game server and responding with a message that shows who is online, how many mods are loaded, etc.

![image](https://user-images.githubusercontent.com/4098674/44004785-1e47ca14-9e2e-11e8-87da-58574c06ab6f.png)

### Setup
1. The server owner navigates to this link https://discordapp.com/oauth2/authorize?client_id=392875945717137418&scope=bot&permissions=0 .
2. Bowser is given read and write permissions on any channels where bowser should respond to commands.

### Usage
Any channel bowser has read and write permissions for, bowser will respond to the command `!help`.  Configuration is currently limited to one minecraft server per discord channel, and the administrator role is able to configure it with `!set <host> <port>`.
