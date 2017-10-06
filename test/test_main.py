from unittest.mock import MagicMock, patch
import asynctest
import discord
import unittest


class TestMain(unittest.TestCase):
    @patch('src.main.main')
    def test__init_calls_main_once(self, mock_main):
        import src.main
        with patch.object(src.main, '__name__', '__main__'):
            src.main.init()
            mock_main.assert_called_once_with()


class TestBot(asynctest.TestCase):
    def setUp(self):
        from src.main import Bot
        self.bot = Bot()
        self.bot.user = MagicMock(
            spec=discord.User,
            id=42,
            name='mock_name',
            bot=self.bot,
        )
        self.mock_run = patch('discord.Client.run')
        self.mock_run.start()

    def tearDown(self):
        self.mock_run.stop()

    @patch('src.main.Minecraft')
    async def test__sends_error_message_when_connection_refused(
            self, mock_mc):
        mock_mc.get_formatted_status_message.side_effect = \
            ConnectionRefusedError
        mock_message = MagicMock(
            spec=discord.Message,
            author=MagicMock(
                spec=discord.User,
                id=800,
                name='mock_user',
            ),
            channel=MagicMock(
                spec=discord.Channel,
            ),
            content='!help',
            mentions=[],
        )
        with asynctest.patch.object(self.bot, 'say') as mock_say:
            await self.bot.on_message(mock_message)
            mock_say.assert_called_once_with(mock_message.content)
