import asyncio
import logging
import os
import discord
import pytest

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope='module')
def loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='module')
def koopa(loop):
    client = discord.Client(loop=loop)
    asyncio.ensure_future(client.login(os.getenv('KOOPA_TOKEN'), bot=True))
    loop.run_until_complete(client.wait_until_login())
    asyncio.ensure_future(client.connect())
    loop.run_until_complete(client.wait_until_ready())
    yield client
    loop.run_until_complete(client.logout())


@pytest.fixture(scope='module')
def server(koopa):
    return discord.utils.find(
        lambda m: m.id == '339549920338116611',
        koopa.servers
    )


@pytest.fixture(scope='module')
def channel(server):
    return discord.utils.find(
        lambda m: m.id == '345543855208267777',
        server.channels
    )


@pytest.fixture(scope='module')
def bowser_testing(server):
    bowser_testing_id = '433111989007417347'
    return discord.utils.find(
        lambda m: m.id == bowser_testing_id,
        server.members
    )


def test_getting_ip_works(loop, channel, koopa, bowser_testing):
    task = loop.create_task(koopa.wait_for_message(author=bowser_testing))
    loop.run_until_complete(koopa.send_message(channel, '!ip'))
    message = loop.run_until_complete(asyncio.wait_for(task, 2))
    assert message.content == 'play.minesuperior.com:25565'
