from .base_hbase_connector_proxy import (
    BaseHbaseConnectorProxy,
    BaseHbaseConnectorProxyConfig
)
from typing import List
from happybase import ConnectionPool
from logger import SingletonLogger


class HbaseConnectorProxyVersion1(BaseHbaseConnectorProxy):
    """
    Class for getting Hbase connection
    Check server status by getting list of tables in Hbase
    """

    def __init__(
            self, servers: List[str], port: int, pool_size: int,
            timeout: int, transport: str, protocol: str
    ):
        """
        Init method
        :param servers: list ip of servers
        :param port: port to read data
        :param pool_size: size of pool
        :param timeout: timeout of connect
        :param transport: transport method
        :param protocol: protocol method
        """
        self.servers = servers
        self.port = port
        self.pool_size = pool_size
        self.timeout = timeout
        self.transport = transport
        self.protocol = protocol
        super(HbaseConnectorProxyVersion1, self).__init__()

    @property
    def servers(self) -> List[str]:
        return self._servers

    @servers.setter
    def servers(self, servers: List[str]):
        assert isinstance(servers, list)
        assert all(map(lambda x: isinstance(x, str), servers))
        self._servers: List[str] = servers

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int):
        assert isinstance(port, int)
        self._port: int = port

    @property
    def pool_size(self) -> int:
        return self._pool_size

    @pool_size.setter
    def pool_size(self, pool_size: int):
        assert isinstance(pool_size, int)
        self._pool_size: int = pool_size

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int):
        assert isinstance(timeout, int)
        self._timeout: int = timeout

    @property
    def transport(self) -> str:
        return self._transport

    @transport.setter
    def transport(self, transport: str):
        assert isinstance(transport, str)
        self._transport: str = transport

    @property
    def protocol(self) -> str:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        assert isinstance(protocol, str)
        self._protocol: str = protocol

    def _create_connection_pool(self):
        """
        Create connection pool to Hbase: set value to self._connection_pool
        :return: None
        """
        for server in self.servers:
            try:
                self._connection_pool = ConnectionPool(
                    size=self.pool_size, host=server, port=self.port,
                    timeout=self.timeout, transport=self.transport,
                    protocol=self.protocol
                )
                if self._check_server_status():
                    return
            except:
                SingletonLogger.get_instance().exception(
                    f"Can not connect to Hbase server {server}"
                )
        self._connection_pool = None

    def _check_server_status(self) -> bool:
        """
        Check status of Hbase server
        :return: True if healthy, else False
        """
        if self._connection_pool is None:
            # No current active server
            return False
        try:
            with self._connection_pool.connection() as connection:
                _: List[bytes] = connection.tables()
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception occur when checking Hbase server status"
            )
            return False


class HbaseConnectorProxyVersion1Config(BaseHbaseConnectorProxyConfig):
    """
    Config class for getting Hbase connection
    Check server status by getting list of tables in Hbase
    """

    def __init__(
            self, servers: List[str], port: int, pool_size: int,
            timeout: int, transport: str, protocol: str
    ):
        """
        Init method
        :param servers: list ip of servers
        :param port: port to read data
        :param pool_size: size of pool
        :param timeout: timeout of connect
        :param transport: transport method
        :param protocol: protocol method
        """
        self.servers = servers
        self.port = port
        self.pool_size = pool_size
        self.timeout = timeout
        self.transport = transport
        self.protocol = protocol
        super(HbaseConnectorProxyVersion1Config, self).__init__()

    @property
    def servers(self) -> List[str]:
        return self._servers

    @servers.setter
    def servers(self, servers: List[str]):
        assert isinstance(servers, list)
        assert all(map(lambda x: isinstance(x, str), servers))
        self._servers: List[str] = servers

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int):
        assert isinstance(port, int)
        self._port: int = port

    @property
    def pool_size(self) -> int:
        return self._pool_size

    @pool_size.setter
    def pool_size(self, pool_size: int):
        assert isinstance(pool_size, int)
        self._pool_size: int = pool_size

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int):
        assert isinstance(timeout, int)
        self._timeout: int = timeout

    @property
    def transport(self) -> str:
        return self._transport

    @transport.setter
    def transport(self, transport: str):
        assert isinstance(transport, str)
        self._transport: str = transport

    @property
    def protocol(self) -> str:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        assert isinstance(protocol, str)
        self._protocol: str = protocol

    def __str__(self) -> str:
        return f"""HbaseConnectorProxyVersion1Config     
                   servers: {';'.join(self.servers)}
                   port: {self.port}
                   pool_size: {self.pool_size}
                   timeout: {self.timeout}
                   transport: {self.transport}
                   protocol: {self.protocol}   
                """

