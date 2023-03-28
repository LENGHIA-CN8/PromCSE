from typing import Optional, List, Tuple, Dict
from objects import User, Post
from .base_user_posts_reader import (
    BaseUserPostsReader, BaseUserPostsReaderConfig
)
from abc import ABC, abstractmethod
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from logger import SingletonLogger
from aerospike import Client


class BaseAerospikeUserPostsReaderVersion1(BaseUserPostsReader, ABC):
    """
    Base class for reading user posts from Ae
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            ae_namespace: str, ae_set: str
    ):
        """
        Init method
        :param connector: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        """
        super(BaseAerospikeUserPostsReaderVersion1, self).__init__()
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

    def _gen_key(self, user: User) -> Tuple[str, str, str]:
        """
        Gen key for user
        :param user: user to get key
        :return: namespace, set, key
        """
        return (
            self.ae_namespace, self.ae_set, str(user.user_id)
        )

    @abstractmethod
    def _convert_bins_to_posts(
            self, bins: Dict
    ) -> Optional[List[Post]]:
        """
        Convert bins to list posts
        :param bins: ae bins
        :return: list of posts or None
        """
        pass

    def read_user(
            self, user: User
    ) -> Optional[List[Post]]:
        """
        Read list posts related to user
        :param user: user to read
        :return: list posts related to user, or None
        """
        try:
            key: Tuple[str, str, str] = self._gen_key(user=user)
            client: Optional[Client] = self.connector.get_client()
            if client is None:
                return None
            _, meta = client.exists(key)
            if meta is None:
                return None
            _, _, bins = client.get(key)
            return self._convert_bins_to_posts(bins=bins)
        except:
            SingletonLogger.get_instance().exception(
                f"Exception while reading user posts from Aerospike"
            )
            return None


class BaseAerospikeUserPostsReaderVersion1Config(BaseUserPostsReaderConfig, ABC):
    """
    Base class for reading user posts from Ae
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            ae_namespace: str, ae_set: str
    ):
        """
        Init method
        :param connector_config: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        """
        super(BaseAerospikeUserPostsReaderVersion1Config, self).__init__()
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
