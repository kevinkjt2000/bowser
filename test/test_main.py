from unittest.mock import MagicMock, patch
import asynctest
import discord
import unittest


class TestMain(unittest.TestCase):
    @patch('src.main.main', return_value=42)
    def test__init_calls_main_once(self, mock_main):
        import src.main
        with patch.object(src.main, '__name__', '__main__'):
            src.main.init()
            mock_main.assert_called_once_with()


class TestBotMain(asynctest.TestCase):
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
