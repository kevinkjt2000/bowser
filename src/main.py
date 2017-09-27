from discord.ext import commands
from Minecraft import Minecraft

description = '''A bot for querying the status of a minecraft server.'''
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description=description,
)


def main():
    bot.add_listener(on_command_error)
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)


async def on_command_error(exception, context):
    if hasattr(exception, 'original'):
        if exception.original.__class__.__name__ == 'ConnectionRefusedError':
            await bot.send_message(
                context.message.channel,
                'The server is not accepting connections at this time.',
            )
    elif exception.__class__.__name__ == 'CommandNotFound':
        pass
    else:
        await bot.send_message(
            context.message.channel,
            'The bot is giving up; something unknown happened.'
        )


@bot.command(description='For getting the status')
async def status():
    await bot.say(Minecraft().get_formatted_status_message())


@bot.command(description='For getting the forge version')
async def forge_version():
    await bot.say(Minecraft().get_forge_version_message())

if __name__ == '__main__':
    main()
