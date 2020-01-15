import os
import pytest
import tempfile

from tests.utils import (
    get_open_port,
)
from web3 import Web3

from .common import (
    CommonGoEthereumShhModuleTest,
    GoEthereumAdminModuleTest,
    GoEthereumEthModuleTest,
    GoEthereumNetModuleTest,
    GoEthereumPersonalModuleTest,
    GoEthereumTest,
    GoEthereumVersionModuleTest,
)
from .utils import (
    wait_for_socket,
)


@pytest.fixture(scope='module')
def geth_command_arguments(geth_ipc_path,
                           base_geth_command_arguments):
    geth_port = get_open_port()
    return (
        base_geth_command_arguments +
        (
            '--port', geth_port,
            '--ipcpath', geth_ipc_path,
        )
    )


@pytest.fixture(scope='module')
def geth_ipc_path(datadir):
    geth_ipc_dir_path = tempfile.mkdtemp()
    _geth_ipc_path = os.path.join(geth_ipc_dir_path, 'geth.ipc')
    yield _geth_ipc_path

    if os.path.exists(_geth_ipc_path):
        os.remove(_geth_ipc_path)


@pytest.fixture(scope="module")
def web3(geth_process, geth_ipc_path):
    wait_for_socket(geth_ipc_path)
    _web3 = Web3(Web3.IPCProvider(geth_ipc_path))
    return _web3


class TestGoEthereumTest(GoEthereumTest):
    pass


class TestGoEthereumAdminModuleTest(GoEthereumAdminModuleTest):
    @pytest.mark.xfail(reason="running geth with the --nodiscover flag doesn't allow peer addition")
    def test_admin_peers(web3):
        super().test_admin_peers(web3)


class TestGoEthereumEthModuleTest(GoEthereumEthModuleTest):
    def test_eth_replaceTransaction_already_mined(self, web3, unlocked_account_dual_type):
        web3.geth.miner.start()
        super().test_eth_replaceTransaction_already_mined(web3, unlocked_account_dual_type)
        web3.geth.miner.stop()


class TestGoEthereumVersionModuleTest(GoEthereumVersionModuleTest):
    pass


class TestGoEthereumNetModuleTest(GoEthereumNetModuleTest):
    pass


class TestGoEthereumPersonalModuleTest(GoEthereumPersonalModuleTest):
    pass


class TestGoEthereumShhModuleTest(CommonGoEthereumShhModuleTest):
    pass
