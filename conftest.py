import pytest

from labgrid.external import HawkbitTestClient

@pytest.fixture(scope='session')
def command(target):
    shell = target.get_driver('CommandProtocol')
    target.activate(shell)
    return shell

@pytest.fixture()
def hawkbit(target):
    client = HawkbitTestClient("localhost", "8080", "admin", "admin")
    assert(isinstance(client, HawkbitTestClient))
    return client
