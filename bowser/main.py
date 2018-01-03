from bowser.Bot import Bot


def main():
    bot = Bot()
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)


def init():
    if __name__ == '__main__':
        main()


init()
