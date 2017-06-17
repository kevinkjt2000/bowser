import discord
from mcstatus import MinecraftServer

client = discord.Client()
servers = [
    MinecraftServer(host='KnightOfficial.Playat.CH', port=25565)
]


@client.event
async def on_message(message):
    if message.content.startswith('!'):
        status = servers[0].status()
        online_players = [p.name for p in status.players.sample]
        online_players = str(online_players).replace("'", '')
        online_count = status.players.online
        max_count = status.players.max
        mods_count = len(status.raw['modinfo']['modList'])
        print(message.content)
        status_message = '{} mods loaded, players {}/{}: {}'.format(
            mods_count, online_count, max_count, online_players)
        await client.send_message(message.channel, status_message)

token = open('token.txt').read().replace('\n', '')
client.run(token)
