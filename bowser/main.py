from bowser.Bot import Bot
import asyncio
loop = asyncio.get_event_loop()


def main():
    bot = Bot()
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)
    loop.run_until_complete(bot.close())


def init():
    if __name__ == '__main__':
        main()


init()
