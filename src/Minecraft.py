from mcstatus import MinecraftServer


class Minecraft:
    def __init__(self, host='msb.teamrapturemc.stream', port=25565,
                 test_server=None):
        if test_server:
            self.mc_server = test_server
        else:
            self.mc_server = MinecraftServer(host=host, port=port)

    def get_formatted_status_message(self):
        status = self.mc_server.status()
        online_players = ', '.join([p.name for p in status.players.sample])
        online_count = status.players.online
        max_count = status.players.max
        mods_count = len(status.raw['modinfo']['modList'])
        status_message = '{} mods loaded, players {}/{}: {}'.format(
            mods_count, online_count, max_count, online_players)
        return status_message
