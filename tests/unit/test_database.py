from unittest.mock import patch
import asynctest
import mockredis
from bowser.database import Database


class TestDatabase(asynctest.TestCase):
    @patch('bowser.database.redis.StrictRedis', mockredis.mock_strict_redis_client)
    def test__able_to_set_and_fetch_data(self):
        db = Database()
        db.set_data_of_server_channel('fake_server_id', 'fake_channel', {'host': 'some_host', 'port': 1234})
        data = db.fetch_data_of_server_channel('fake_server_id', 'fake_channel')
        assert data['host'] == 'some_host'
        assert data['port'] == 1234
