from discord.ext import commands
from mcstatus import MinecraftServer

description = '''A bot for querying the status of a minecraft server.'''
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description=description,
)


def main():
    bot.add_listener(on_command_error)
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)


def get_formatted_status_message(minecraft_server=MinecraftServer(
        host='KnightOfficial.Playat.CH', port=25565)):
    status = minecraft_server.status()
    online_players = ', '.join([p.name for p in status.players.sample])
    online_count = status.players.online
    max_count = status.players.max
    mods_count = len(status.raw['modinfo']['modList'])
    status_message = '{} mods loaded, players {}/{}: {}'.format(
        mods_count, online_count, max_count, online_players)
    return status_message


async def on_command_error(exception, context):
    if str(context.command) == 'status':
        await bot.send_message(
            context.message.channel,
            'The server is not accepting connections at this time.',
        )
    else:
        await bot.send_message(
            context.message.channel,
            'I do not recognize that command.',
        )


@bot.command(description='For getting the status')
async def status():
    await bot.say(get_formatted_status_message())

if __name__ == '__main__':
    main()
