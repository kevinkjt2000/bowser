from mcstatus import MinecraftServer


class Minecraft:
    def __init__(self, host='msb.teamrapturemc.stream', port=25456,
                 test_server=None):
        if test_server:
            self.mc_server = test_server
        else:
            self.mc_server = MinecraftServer(host=host, port=port)

    def get_formatted_status_message(self):
        status = self.mc_server.status()
        if status.players.online > 0:
            online_players = ', '.join([p.name for p in status.players.sample])
        else:
            online_players = ''
        online_count = status.players.online
        max_count = status.players.max
        status_message = ''
        if 'modinfo' in status.raw:
            mods_count = len(status.raw['modinfo']['modList'])
            status_message += '{} mods loaded, '.format(mods_count)
        status_message += 'players {}/{}: {}'.format(
            online_count, max_count, online_players)
        return status_message
