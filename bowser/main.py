from bowser.Bot import Bot


def main():
    bot = Bot()
    try:
        token = open('token.txt').read().replace('\n', '')
        bot.run(token)
    except Exception as ex:
        bot.loop.run_until_complete(bot.close())
        raise ex


def init():
    if __name__ == '__main__':
        main()


init()
