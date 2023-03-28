from typing import Optional, List
from logger import SingletonLogger
from objects import User
from .base_all_users_reader import (
    BaseAllUsersReader, BaseAllUsersReaderConfig
)
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from aerospike import Client, Scan


class AerospikeAllUsersReaderVersion1(BaseAllUsersReader):
    """
    Read users from Aerospike
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            ae_namespace: str, ae_set: str
    ):
        """
        Init method
        :param connector: connection to Ae
        :param ae_namespace: namespace to connect to Ae
        :param ae_set: set to connect to Ae
        """
        super().__init__()
        self.connector = connector
        self.ae_namespace = ae_namespace
        self.ae_set = ae_set

    @property
    def connector(self) -> BaseAerospikeConnectorProxy:
        return self._connector

    @connector.setter
    def connector(self, connector: BaseAerospikeConnectorProxy):
        assert isinstance(connector, BaseAerospikeConnectorProxy)
        self._connector: BaseAerospikeConnectorProxy = connector

    @property
    def ae_namespace(self) -> str:
        return self._ae_namespace

    @ae_namespace.setter
    def ae_namespace(self, ae_namespace: str):
        assert isinstance(ae_namespace, str)
        self._ae_namespace: str = ae_namespace

    @property
    def ae_set(self) -> str:
        return self._ae_set

    @ae_set.setter
    def ae_set(self, ae_set: str):
        assert isinstance(ae_set, str)
        self._ae_set: str = ae_set

    def read_users(self) -> Optional[List[User]]:
        """
        Read list of users
        :return: list of users or None
        """
        try:
            client: Optional[Client] = self.connector.get_client()
            if client is None:
                # can not get connection
                return None
            users: List[User] = []

            def add_user(record):
                key, _, _ = record
                user_id = key[2]
                if (
                    not isinstance(user_id, str) or
                    not user_id.isdigit()
                ):
                    return None
                user = User(user_id=int(user_id))
                users.append(user)

            scan: Scan = client.scan(self.ae_namespace, self.ae_set)
            scan.foreach(callback=add_user)
            return users
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading users from Aerospike"
            )
            return None


class AerospikeAllUsersReaderVersion1Config(BaseAllUsersReaderConfig):
    """
    Read users from Aerospike
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            ae_namespace: str, ae_set: str
    ):
        """
        Init method
        :param connector_config: connection to Ae
        :param ae_namespace: namespace to connect to Ae
        :param ae_set: set to connect to Ae
        """
        super().__init__()
        self.connector_config = connector_config
        self.ae_namespace = ae_namespace
        self.ae_set = ae_set

    @property
    def connector_config(self) -> BaseAerospikeConnectorProxyConfig:
        return self._connector_config

    @connector_config.setter
    def connector_config(self, connector_config: BaseAerospikeConnectorProxyConfig):
        assert isinstance(connector_config, BaseAerospikeConnectorProxyConfig)
        self._connector_config: BaseAerospikeConnectorProxyConfig = connector_config

    @property
    def ae_namespace(self) -> str:
        return self._ae_namespace

    @ae_namespace.setter
    def ae_namespace(self, ae_namespace: str):
        assert isinstance(ae_namespace, str)
        self._ae_namespace: str = ae_namespace

    @property
    def ae_set(self) -> str:
        return self._ae_set

    @ae_set.setter
    def ae_set(self, ae_set: str):
        assert isinstance(ae_set, str)
        self._ae_set: str = ae_set
