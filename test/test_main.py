from unittest.mock import patch
import asynctest
import discord
import random
import unittest
import src.main


class TestMain(unittest.TestCase):
    @patch('src.main.main')
    def test__init_calls_main_once(self, mock_main):
        with patch.object(src.main, '__name__', '__main__'):
            src.main.init()
            mock_main.assert_called_once_with()


class TestBot(asynctest.TestCase):
    def setUp(self):
        self.bot = src.main.Bot()
        self.bot.user = self._get_mock_user(bot=True)
        self.mock_server_id = str(random.randrange(999999))
        self.mock_run = asynctest.patch.object(self.bot, 'run')
        self.mock_run.start()

    def tearDown(self):
        self.mock_run.stop()

    async def test__sends_error_message_when_connection_refused(self):
        mock_channel_id = str(random.randrange(999999))
        with asynctest.patch('src.main.minecrafts', {
            self.mock_server_id: {
                mock_channel_id: asynctest.MagicMock(
                    spec=src.Minecraft.Minecraft,
                ),
            },
        }) as mock_minecrafts:
            mock_mc = mock_minecrafts[self.mock_server_id][mock_channel_id]
            mock_message = self._get_mock_message(
                '!status',
                channel=mock_channel_id,
            )
            with asynctest.patch.object(self.bot, 'say') as mock_say:
                await self.bot.on_message(mock_message)
                mock_mc.get_formatted_status_message.assert_called_once()
                mock_say.assert_called_once_with(
                    mock_mc.get_formatted_status_message()
                )

    def _get_mock_channel(self, **kwargs):
        id = kwargs.pop('id', str(random.randrange(999999)))
        return asynctest.MagicMock(
            spec=discord.Channel,
            id=id,
        )

    def _get_mock_server(self):
        return asynctest.MagicMock(
            spec=discord.Server,
            id=self.mock_server_id,
            me=self.bot.user,
        )

    def _get_mock_message(self, content, **kwargs):
        channel = kwargs.pop('channel', self._get_mock_channel())
        server = kwargs.pop('server', self._get_mock_server())
        if type(channel) is str:
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
            spec=discord.User,
            id=str(random.randrange(999999)),
            name='mock_user',
            bot=bot,
        )
