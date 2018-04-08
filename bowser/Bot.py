from discord.ext import commands
from discord.ext.commands.core import Command
from bowser.Database import Database
from bowser.Minecraft import Minecraft


class Bot(commands.Bot):
    def _get_game_data(self, context):
        sid = str(context.message.server.id)
        cid = str(context.message.channel.id)
        data = self.db.fetch_data_of_server_channel(sid, cid)
        mc = Minecraft(**data)
        return mc

    def _command(self, help, checks=None, name=None, get_mc=True):
        def decorator(function):
            async def wrapped(context, *args):
                if get_mc:
                    mc = self._get_game_data(context)
                    return await function(self, mc, *args)
                else:
                    return await function(self, *args)

            self.add_command(
                Command(
                    name=name or function.__name__,
                    callback=wrapped,
                    help=help,
                    pass_context=True,
                    checks=checks,
                ))

        return decorator

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            description="""
            A bot for querying minecraft server stuff.
            https://github.com/kevinkjt2000/bowser""",
        )
        self.db = Database()

        def is_admin(context):
            return context.message.author.top_role.permissions.administrator

        @self._command('Sets the host and port for this channel.', name='set', checks=[is_admin], get_mc=False)
        async def set_info(self, host, port):
            await self.say(f'Finished adding `{host}:{port}`.  Try `!status` now.')

        @self._command('Gets the MOTD.')
        async def motd(self, mc):
            motd = mc.get_motd()
            await self.say(motd)

        @self._command('Number of mods loaded and who is online.')
        async def status(self, mc):
            status_msg = mc.get_formatted_status_message()
            await self.say(status_msg)

        @self._command('The forge version.')
        async def forge_version(self, mc):
            forge_ver_msg = mc.get_forge_version_message()
            await self.say(forge_ver_msg)

        @self._command('The IP and port of the server.')
        async def ip(self, mc):
            ip_msg = f'{mc.mc_server.host}:{mc.mc_server.port}'
            await self.say(ip_msg)

        print('Bowser is ready!')

    async def on_command_error(self, exception, context):
        if exception.__class__.__name__ == 'CommandNotFound':
            pass
        elif exception.__class__.__name__ == 'CheckFailure':
            await self.send_message(
                context.message.channel,
                'You do not have permission to run this command.',
            )
        elif not hasattr(exception, 'original'):
            print('unknown: ' + exception.__class__.__name__)
            print(exception)
            await self.send_message(
                context.message.channel,
                'The bot is giving up; something unknown happened.',
            )
        else:
            original = exception.original.__class__.__name__
            if original == 'ConnectionRefusedError' or original == 'timeout':
                await self.send_message(
                    context.message.channel,
                    'The server is not accepting connections at this time.',
                )
            elif original == 'gaierror':
                await self.send_message(
                    context.message.channel,
                    'The !ip is unreachable; complain to someone in charge.',
                )
            elif original == 'OSError':
                await self.send_message(
                    context.message.channel,
                    'Server did not respond with any information.',
                )
            elif original == 'KeyError':
                await self.send_message(
                    context.message.channel,
                    'There is not yet a Minecraft server configured for this'
                    ' discord server channel.',
                )
            else:
                print('original: ' + original)
                print(exception)
                print(f'command: {context.invoked_with}')
                sid = context.message.server.id
                cid = context.message.channel.id
                print(f'sid: {sid} cid: {cid}')
                await self.send_message(
                    context.message.channel,
                    'Ninjas hijacked the packets, but the author will fix it.',
                )
