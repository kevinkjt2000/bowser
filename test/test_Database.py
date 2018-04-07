from unittest.mock import patch
import asynctest
import mockredis
from bowser.Database import Database


class TestDatabase(asynctest.TestCase):
    @patch('bowser.Database.redis.StrictRedis', mockredis.mock_strict_redis_client)
    def test__able_to_set_and_fetch_server_data(self):
        db = Database()
        db.set_data_of_server('fake_server_id', 'stuff')
        data = db.fetch_data_of_server('fake_server_id')
        assert data == b'stuff'
