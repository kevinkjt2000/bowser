from discord.ext import commands
from bowser.database import Database
from bowser.minecraft import Minecraft


def _set_permission(context):
    perms = context.message.channel.permissions_for(context.message.author)
    is_owner = None
    try:
        is_owner = context.message.author == context.message.server.owner
    except AttributeError:
        pass
    return any([
        getattr(perms, 'administrator', None),
        getattr(perms, 'manage_channels', None),
        getattr(perms, 'manage_server', None),
        is_owner,
    ])


class Bowser():
    def _get_game_data(self, context):
        sid = None
        try:
            sid = str(context.message.server.id)
        except AttributeError:
            pass
        cid = str(context.message.channel.id)
        data = self.db.fetch_data_of_server_channel(sid, cid)
        return Minecraft(**data)

    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        print('Bowser is ready!')

    @commands.command(name='set', pass_context=True)
    @commands.check(_set_permission)
    async def set_info(self, context, host, port: int):
        '''Sets the host and port for this channel.'''
        sid = str(context.message.server.id)
        cid = str(context.message.channel.id)
        self.db.set_data_of_server_channel(sid, cid, {'host': host, 'port': port})
        await self.bot.say(f'Finished adding `{host}:{port}`.  Try `!status` now.')

    @commands.command(pass_context=True)
    async def motd(self, context):
        '''Gets the MOTD.'''
        mc = self._get_game_data(context)
        motd = mc.get_motd()
        await self.bot.say(motd)

    @commands.command(pass_context=True)
    async def status(self, context):
        '''Number of mods loaded and who is online.'''
        mc = self._get_game_data(context)
        status_msg = mc.get_formatted_status_message()
        await self.bot.say(status_msg)

    @commands.command(pass_context=True)
    async def forge_version(self, context):
        '''The forge version.'''
        mc = self._get_game_data(context)
        forge_ver_msg = mc.get_forge_version_message()
        await self.bot.say(forge_ver_msg)

    @commands.command(pass_context=True)
    async def ip(self, context):
        '''The IP and port of the server.'''
        mc = self._get_game_data(context)
        ip_msg = f'{mc.mc_server.host}:{mc.mc_server.port}'
        await self.bot.say(ip_msg)

    async def on_command_error(self, exception, context):
        if exception.__class__.__name__ == 'CommandNotFound':
            pass
        elif exception.__class__.__name__ == 'CheckFailure':
            await self.bot.send_message(
                context.message.channel,
                'You do not have permission to run this command.',
            )
        elif exception.__class__.__name__ == 'MissingRequiredArgument':
            await self.bot.send_message(
                context.message.channel,
                f'Not enough arguments.  Try `!help {context.invoked_with}` for more information.',
            )
        elif not hasattr(exception, 'original'):
            print('unknown: ' + exception.__class__.__name__)
            print(exception)
            await self.bot.send_message(
                context.message.channel,
                'The bot is giving up; something unknown happened.',
            )
        else:
            original = exception.original.__class__.__name__
            if original == 'ConnectionRefusedError' or original == 'timeout':
                await self.bot.send_message(
                    context.message.channel,
                    'The server is not accepting connections at this time.',
                )
            elif original == 'gaierror':
                await self.bot.send_message(
                    context.message.channel,
                    'The !ip is unreachable; complain to someone in charge.',
                )
            elif original == 'OSError':
                await self.bot.send_message(
                    context.message.channel,
                    'Server did not respond with any information.',
                )
            elif original == 'KeyError':
                await self.bot.send_message(
                    context.message.channel,
                    'There is not yet a Minecraft server configured for this'
                    ' discord server channel.',
                )
            else:
                print('original: ' + original)
                print(exception)
                print(f'command: {context.invoked_with}')
                sid = None
                try:
                    sid = context.message.server.id
                except AttributeError:
                    pass
                cid = context.message.channel.id
                print(f'sid: {sid} cid: {cid}')
                await self.bot.send_message(
                    context.message.channel,
                    'Ninjas hijacked the packets, but the author will fix it.',
                )


def setup(bot):
    bot.add_cog(Bowser(bot))
