import redis


class Database(object):
    def __init__(self):
        self.redis = redis.StrictRedis(host='redis', port=6379, db=0)

    def set_data_of_server(self, server_id, data):
        self.redis.set(server_id, data)

    def fetch_data_of_server(self, server_id):
        return self.redis.get(server_id)
