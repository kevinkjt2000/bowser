import asyncio
import os
from discord.ext import commands
from retrying import retry
loop = asyncio.get_event_loop()


def retry_if_connection_reset(exception):
    return isinstance(exception, ConnectionResetError)


bowser = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description="""
    A bot for querying minecraft server stuff.
    https://github.com/kevinkjt2000/bowser""",
)


@retry(retry_on_exception=retry_if_connection_reset, wait_fixed=1000)
def main():
    try:
        token = os.getenv(
            'BOWSER_TOKEN',
            open('token.txt').read().replace('\n', '')
        )
        bowser.load_extension('bowser.bowser')
        bowser.run(token)
    finally:
        loop.run_until_complete(bowser.close())


def init():
    if __name__ == '__main__':
        main()


init()
