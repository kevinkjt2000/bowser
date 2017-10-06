from discord.ext import commands
from discord.ext.commands.core import Command
from src.Minecraft import Minecraft


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            description='A bot for querying the status of a minecraft server.'
        )
        self.mc = Minecraft()
        self.add_command(Command(
            name='status',
            callback=self.status,
            description='For getting the status',
        ))
        self.add_command(Command(
            name='forge_version',
            callback=self.forge_version,
            description='For getting the forge version',
        ))

    async def on_command_error(self, exception, context):
        if hasattr(exception, 'original'):
            original = exception.original.__class__.__name__
            if original == 'ConnectionRefusedError':
                await self.send_message(
                    context.message.channel,
                    'The server is not accepting connections at this time.',
                )
        if exception.__class__.__name__ == 'CommandNotFound':
            pass
        elif exception.__class__.__name__ == 'CommandInvokeError':
            await self.send_message(
                context.message.channel,
                'The server is not fully ready for connections yet.'
            )
        else:
            print('unknown: ' + exception.__class__.__name__)
            print(exception)
            await self.send_message(
                context.message.channel,
                'The bot is giving up; something unknown happened.'
            )

    async def status(self):
        await self.say(self.mc.get_formatted_status_message())

    async def forge_version(self):
        await self.say(self.mc.get_forge_version_message())


def main():
    bot = Bot()
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)


def init():
    if __name__ == '__main__':
        main()


init()
