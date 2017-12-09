from unittest.mock import patch, mock_open
import unittest
import src.main


class TestMain(unittest.TestCase):
    @patch('src.main.main')
    def test__init_calls_main_once(self, mock_main):
        with patch.object(src.main, '__name__', '__main__'):
            src.main.init()
            mock_main.assert_called_once_with()

    @patch('src.main.Bot.run')
    @patch('builtins.open', new_callable=mock_open, read_data='mock_token')
    def test__main_starts_the_bot(self, mock_open, mock_bot_run):
        src.main.main()
        mock_bot_run.assert_called_once_with('mock_token')
