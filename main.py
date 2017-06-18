from discord.ext import commands
from mcstatus import MinecraftServer

description = '''A bot for querying the status of a minecraft server.'''
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description=description,
)
servers = [
    MinecraftServer(host='KnightOfficial.Playat.CH', port=25565),
]


@bot.command(description='For getting the status')
async def status():
    async def on_command_error(exception, context):
        await bot.send_message(
            context.message.channel,
            'The server is not accepting connections at this time',
        )
    bot.add_listener(on_command_error)
    status = servers[0].status()
    online_players = [p.name for p in status.players.sample]
    online_players = str(online_players).replace("'", '')
    online_count = status.players.online
    max_count = status.players.max
    mods_count = len(status.raw['modinfo']['modList'])
    status_message = '{} mods loaded, players {}/{}: {}'.format(
        mods_count, online_count, max_count, online_players)
    await bot.say(status_message)

token = open('token.txt').read().replace('\n', '')
bot.run(token)
