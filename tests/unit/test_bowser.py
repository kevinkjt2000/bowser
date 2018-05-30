from unittest.mock import patch
import asyncio
import random
import string
import asynctest
import discord
from discord.ext import commands
import mockredis
from bowser.bowser import Bowser


class HelperFunctions(asynctest.TestCase):
    async def setUp(self):
        self.server_id = str(random.randrange(999999))

        patch_db = patch('bowser.database.redis.StrictRedis', mockredis.mock_strict_redis_client)
        patch_db.start()
        self.addCleanup(patch_db.stop)

        self.patch_mc = patch('bowser.bowser.Minecraft')
        self.mock_mc = self.patch_mc.start()
        self.mock_mc.side_effect = []
        self.addCleanup(self.patch_mc.stop)

        self.bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))
        self.bowser = Bowser(self.bot)
        self.bot.add_cog(self.bowser)
        self.bot.user = self._get_mock_user(bot=True)

        patch_run = asynctest.patch.object(self.bot, 'run')
        patch_run.start()
        self.addCleanup(patch_run.stop)

        patch_send = asynctest.patch.object(self.bot, 'send_message')
        self.mock_send = patch_send.start()
        self.addCleanup(patch_send.stop)

        self.games = []
        self._add_game_channel()

    async def tearDown(self):
        await self.bot.close()

    def _add_game_channel(self):
        game = {
            'server_id': self.server_id,
            'channel_id': str(random.randrange(999999)),
            'host': ''.join(random.choice(string.ascii_lowercase) for _ in range(10)),
            'port': random.randrange(65535),
        }
        self.bowser.db.set_data_of_server_channel(
            game['server_id'],
            game['channel_id'],
            {'host': game['host'], 'port': game['port']},
        )
        game['mock'] = asynctest.MagicMock()
        self.mock_mc.side_effect = list(self.mock_mc.side_effect) + [game['mock']]
        self.games.append(game)

    def _get_mock_command_message(self, command):
        return self._get_mock_message(command, channel=self.games[0]['channel_id'])

    def _get_mock_channel(self, **kwargs):
        id = kwargs.pop('id', str(random.randrange(999999)))
        return asynctest.MagicMock(
            spec=discord.Channel,
            id=id,
        )

    def _get_mock_server(self):
        return asynctest.MagicMock(
            spec=discord.Server,
            id=self.games[0]['server_id'],
            me=self.bot.user,
        )

    def _get_mock_message(self, content, **kwargs):
        channel = kwargs.pop('channel', self._get_mock_channel())
        server = kwargs.pop('server', self._get_mock_server())
        if isinstance(channel, str):
            channel = self._get_mock_channel(id=channel)
        return asynctest.MagicMock(
            spec=discord.Message,
            author=self._get_mock_user(),
            channel=channel,
            server=server,
            content=content,
            mentions=[],
        )

    def _get_mock_user(self, bot=None):
        return asynctest.MagicMock(
            spec=discord.Member,
            id=str(random.randrange(999999)),
            name='mock_user',
            bot=bot,
        )


class TestBowser(HelperFunctions):
    async def test__statuses_command_works(self):
        self._add_game_channel()
        self._add_game_channel()
        self.games[1]['mock'].get_formatted_status_message.side_effect = Exception
        mock_message = self._get_mock_command_message('!statuses')
        await self.bot.on_message(mock_message)
        await asyncio.sleep(0.02)

        expected_statuses = []
        for game in self.games:
            try:
                status = game['mock'].get_formatted_status_message()
            except Exception:
                status = '<error message goes here>'
            expected_statuses.append(f"{game['host']} {status}")

        self.mock_send.assert_called_once_with(
            mock_message.channel,
            '\n'.join(expected_statuses),
        )

    async def test__support_dms_by_ignoring_attribute_errors(self):
        mock_message = self._get_mock_command_message('!help')
        mock_message.server = None
        await self.bot.on_message(mock_message)
        await asyncio.sleep(0.02)
        assert self.mock_send.call_count == 1

        mock_message = self._get_mock_command_message('!ip')
        mock_message.server = None
        await self.bot.on_message(mock_message)
        await asyncio.sleep(0.02)
        assert self.mock_send.call_count == 2

    async def test__command_missing_arguments_prints_how_to_get_help(self):
        mock_message = self._get_mock_command_message('!set not_enough')
        mock_message.channel.permissions_for.return_value = discord.permissions.Permissions()
        mock_message.channel.permissions_for.return_value.administrator = True
        await self.bot.on_message(mock_message)
        await asyncio.sleep(0.02)
        self.mock_send.assert_called_once_with(
            mock_message.channel,
            f'Not enough arguments.  Try `!help set` for more information.',
        )

    async def test__owner_can_add_a_server(self):
        mock_message = self._get_mock_command_message(f"!set {self.games[0]['host']} {self.games[0]['port']}")
        mock_message.channel.permissions_for.return_value = discord.permissions.Permissions()
        mock_message.author = mock_message.server.owner
        await self.bot.on_message(mock_message)
        await asyncio.sleep(0.02)
        self.mock_send.assert_called_once_with(
            mock_message.channel,
            f"Finished adding `{self.games[0]['host']}:{self.games[0]['port']}`.  Try `!status` now.",
        )

    async def test__nonadmin_cannot_add_a_server(self):
        mock_message = self._get_mock_command_message('!set fake.com 1234')
        mock_message.channel.permissions_for.return_value = discord.permissions.Permissions()
        await self.bot.on_message(mock_message)
        await asyncio.sleep(0.02)
        self.mock_send.assert_called_once_with(
            mock_message.channel,
            'You do not have permission to run this command.',
        )

    async def test__can_fetch_motd(self):
        mock_message = self._get_mock_command_message('!motd')
        await self.bot.on_message(mock_message)
        self.games[0]['mock'].get_motd.assert_called_once()
        self.mock_send.assert_called_once_with(
            mock_message.channel,
            self.games[0]['mock'].get_motd(),
        )

    async def test__can_fetch_forge_version(self):
        mock_message = self._get_mock_command_message('!forge_version')
        await self.bot.on_message(mock_message)
        self.games[0]['mock'].get_forge_version_message.assert_called_once()
        self.mock_send.assert_called_once_with(
            mock_message.channel,
            self.games[0]['mock'].get_forge_version_message(),
        )

    async def test__errors_in_command_execution_are_logged(self):
        self.games[0]['mock'].get_formatted_status_message.side_effect = Exception
        await self._assert_status_command_responds_with(
            'Ninjas hijacked the packets, but the author will fix it.')

    async def test__tells_the_user_when_the_ip_is_bad(self):
        from socket import gaierror
        self.games[0]['mock'].get_formatted_status_message.side_effect = gaierror
        await self._assert_status_command_responds_with(
            'The !ip is unreachable; complain to someone in charge.')

    async def test__bot_gives_up_on_discord_command_errors(self):
        self.games[0]['mock'].get_formatted_status_message.side_effect = \
            discord.ext.commands.errors.CommandError
        await self._assert_status_command_responds_with(
            'The bot is giving up; something unknown happened.')

    async def test__command_not_found_is_ignored(self):
        mock_message = self._get_mock_command_message('!lalala')
        await self.bot.on_message(mock_message)
        self.mock_send.assert_not_called()

    async def test__ip_command_responds_with_host_and_port(self):
        mock_message = self._get_mock_command_message('!ip')
        await self.bot.on_message(mock_message)
        self.mock_send.assert_called_once_with(
            mock_message.channel,
            f"{self.games[0]['mock'].mc_server.host}:{self.games[0]['mock'].mc_server.port}",
        )

    async def test__status_command_warns_about_missing_server(self):
        mock_message = self._get_mock_command_message('!status')
        mock_message.channel = self._get_mock_channel(id='some unconfigured channel')
        await self.bot.on_message(mock_message)
        self.games[0]['mock'].get_formatted_status_message.assert_not_called()
        await asyncio.sleep(0.02)
        self.mock_send.assert_called_once_with(mock_message.channel,
            'There is not yet a Minecraft server configured for this discord'
            ' server channel.')

    async def test__status_command_when_the_server_does_not_respond(self):
        self.games[0]['mock'].get_formatted_status_message.side_effect = OSError
        await self._assert_status_command_responds_with(
            'Server did not respond with any information.')

    async def test__status_command_responds_even_with_connection_errors(self):
        self.games[0]['mock'].get_formatted_status_message.side_effect = \
            ConnectionRefusedError
        await self._assert_status_command_responds_with(
            'The server is not accepting connections at this time.')

    async def test__status_command_responds_with_status_message(self):
        msg = self.games[0]['mock'].get_formatted_status_message()
        self.games[0]['mock'].get_formatted_status_message.reset_mock()
        await self._assert_status_command_responds_with(msg)

    async def _assert_status_command_responds_with(self, message):
        mock_message = self._get_mock_command_message('!status')
        await self.bot.on_message(mock_message)
        self.games[0]['mock'].get_formatted_status_message.assert_called_once()
        await asyncio.sleep(0.02)
        self.mock_send.assert_called_once_with(mock_message.channel, message)
