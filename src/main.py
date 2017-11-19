from discord.ext import commands
from discord.ext.commands.core import Command
from src.Minecraft import Minecraft
import json


def get_minecraft_object_for_server_channel(sid, cid):
    sid = str(sid)
    cid = str(cid)
    minecrafts = {}
    with open('servers.json') as json_data:
        minecrafts = json.load(json_data)
    for s in minecrafts:
        for c in minecrafts[sid]:
            if s == sid and c == cid:
                m = minecrafts[sid][cid]
                return Minecraft(host=m['host'], port=m['port'])
    return None


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            description='A bot for querying the status of a minecraft server.'
        )
        self.add_command(Command(
            name='status',
            callback=self.status,
            description='For getting the status',
            pass_context=True,
        ))
        self.add_command(Command(
            name='forge_version',
            callback=self.forge_version,
            description='For getting the forge version',
            pass_context=True,
        ))
        self.add_command(Command(
            name='ip',
            callback=self.ip,
            description='For getting the ip and port of the server',
            pass_context=True,
        ))

    async def on_command_error(self, exception, context):
        if exception.__class__.__name__ == 'CommandNotFound':
            pass
        elif not hasattr(exception, 'original'):
            print('unknown: ' + exception.__class__.__name__)
            print(exception)
            await self.send_message(
                context.message.channel,
                'The bot is giving up; something unknown happened.'
            )
        else:
            original = exception.original.__class__.__name__
            if original == 'ConnectionRefusedError' or original == 'timeout':
                await self.send_message(
                    context.message.channel,
                    'The server is not accepting connections at this time.',
                )
            else:
                print('original: ' + original)
                print(exception)

    async def status(self, context):
        sid = context.message.server.id
        cid = context.message.channel.id
        mc = get_minecraft_object_for_server_channel(sid, cid)
        if mc:
            status_msg = mc.get_formatted_status_message()
            await self.say(status_msg)

    async def forge_version(self, context):
        sid = context.message.server.id
        cid = context.message.channel.id
        mc = get_minecraft_object_for_server_channel(sid, cid)
        if mc:
            forge_ver_msg = mc.get_forge_version_message()
            await self.say(forge_ver_msg)

    async def ip(self, context):
        sid = context.message.server.id
        cid = context.message.channel.id
        mc = get_minecraft_object_for_server_channel(sid, cid)
        if mc:
            ip_msg = f'{mc.mc_server.host}:{mc.mc_server.port}'
            await self.say(ip_msg)


def main():
    bot = Bot()
    token = open('token.txt').read().replace('\n', '')
    bot.run(token)


def init():
    if __name__ == '__main__':
        main()


init()
