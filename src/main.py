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
    await bot.say(Minecraft().get_formatted_status_message())

if __name__ == '__main__':
    main()
