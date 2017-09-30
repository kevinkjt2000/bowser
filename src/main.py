from discord.ext import commands
from .Minecraft import Minecraft


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            description='A bot for querying the status of a minecraft server.'
        )

    async def on_command_error(self, exception, context):
        if hasattr(exception, 'original'):
            if exception.original.__class__.__name__ == 'ConnectionRefusedError':
                await self.send_message(
                    context.message.channel,
                    'The server is not accepting connections at this time.',
                )
        if exception.__class__.__name__ == 'CommandNotFound':
            pass
        else:
            await self.send_message(
                context.message.channel,
                'The bot is giving up; something unknown happened.'
            )


bot = Bot()


@bot.command(description='For getting the status')
async def status(self):
    await self.say(Minecraft().get_formatted_status_message())


@bot.command(description='For getting the forge version')
async def forge_version(self):
    await self.say(Minecraft().get_forge_version_message())


def main():
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)


if __name__ == '__main__':
    main()
