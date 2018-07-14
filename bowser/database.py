import json
import redis


class Database(object):
    def __init__(self):
        self.redis = redis.StrictRedis(host='redis', port=6379, db=0)

    def fetch_datas_of_server(self, server):
        datas = self.redis.hvals(server)
        json_datas = [json.loads(data.decode('utf-8')) for data in datas]
        return json_datas

    def set_data_of_server_channel(self, server, channel, data):
        self.redis.hmset(server, {channel: json.dumps(data)})

    def fetch_data_of_server_channel(self, server, channel):
        data = self.redis.hget(server, channel)
        if data is None:
            raise KeyError
        json_data = json.loads(data.decode('utf-8'))
        return json_data
