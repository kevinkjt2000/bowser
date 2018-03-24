import asyncio
from bowser.Bot import Bot
from retrying import retry
loop = asyncio.get_event_loop()


def retry_if_connection_reset(exception):
    return isinstance(exception, ConnectionResetError)


@retry(retry_on_exception=retry_if_connection_reset, wait_fixed=1000)
def main():
    bot = Bot()
    try:
        token = open('token.txt').read().replace('\n', '')
        bot.run(token)
    finally:
        loop.run_until_complete(bot.close())


def init():
    if __name__ == '__main__':
        main()


init()
