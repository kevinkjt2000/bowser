from discord.ext import commands
from discord.ext.commands import core
from bowser.Database import Database
from bowser.Minecraft import Minecraft


class Bot(commands.Bot):
    def _get_game_data(self, context):
        sid = str(context.message.server.id)
        cid = str(context.message.channel.id)
        data = self.db.fetch_data_of_server_channel(sid, cid)
        return Minecraft(**data)

    def _command(self, name=None):
        def decorator(function):
            async def wrapped(context, *args):
                return await function(self, context, *args)

            try:
                wrapped.__commands_checks__ = function.__commands_checks__
            except AttributeError:
                pass

            self.command(
                name=name or function.__name__,
                pass_context=True,
            )(wrapped)

        return decorator

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            description="""
            A bot for querying minecraft server stuff.
            https://github.com/kevinkjt2000/bowser""",
        )
        self.db = Database()

        @self._command(name='set')
        @commands.has_permissions(administrator=True)
        async def set_info(self, context, host, port: int):
            '''Sets the host and port for this channel.'''
            sid = str(context.message.server.id)
            cid = str(context.message.channel.id)
            self.db.set_data_of_server_channel(sid, cid, {'host': host, 'port': port})
            await self.say(f'Finished adding `{host}:{port}`.  Try `!status` now.')

        @self._command()
        async def motd(self, context):
            '''Gets the MOTD.'''
            mc = self._get_game_data(context)
            motd = mc.get_motd()
            await self.say(motd)

        @self._command()
        async def status(self, context):
            '''Number of mods loaded and who is online.'''
            mc = self._get_game_data(context)
            status_msg = mc.get_formatted_status_message()
            await self.say(status_msg)

        @self._command()
        async def forge_version(self, context):
            '''The forge version.'''
            mc = self._get_game_data(context)
            forge_ver_msg = mc.get_forge_version_message()
            await self.say(forge_ver_msg)

        @self._command()
        async def ip(self, context):
            '''The IP and port of the server.'''
            mc = self._get_game_data(context)
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
