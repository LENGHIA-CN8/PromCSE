from objects import Post
from .base_post_writer import (
    BasePostWriter, BasePostWriterConfig
)
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from typing import Tuple, List, Dict, Optional
from logger import SingletonLogger
from aerospike import Client
from abc import ABC, abstractmethod


class BaseAerospikePostWriterVersion1(BasePostWriter, ABC):
    """
    Write posts to Aerospike
    All posts will be saved in a pre-defined key
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            key: Tuple[str, str, str], time_to_live: int
    ):
        """
        Init method
        :param connector: connection to Aerospike
        :param key: key in Aerospike to store posts
        :param time_to_live: time to live in Aerospike
        """
        super(BaseAerospikePostWriterVersion1, self).__init__()
        self.connector = connector
        self.key = key
        self.time_to_live = time_to_live

    @property
    def connector(self) -> BaseAerospikeConnectorProxy:
        return self._connector

    @connector.setter
    def connector(self, connector: BaseAerospikeConnectorProxy):
        assert isinstance(connector, BaseAerospikeConnectorProxy)
        self._connector: BaseAerospikeConnectorProxy = connector

    @property
    def key(self) -> Tuple[str, str, str]:
        return self._key

    @key.setter
    def key(self, key: Tuple[str, str, str]):
        assert isinstance(key, tuple)
        assert len(key) == 3
        assert all(map(lambda x: isinstance(x, str),
                       key))
        self._key: Tuple[str, str, str] = key

    @property
    def time_to_live(self) -> int:
        return self._time_to_live

    @time_to_live.setter
    def time_to_live(self, time_to_live: int):
        assert isinstance(time_to_live, int)
        self._time_to_live: int = time_to_live

    def write_post(self, post: Post) -> bool:
        """
        Write a post
        :param post: post to write
        :return: True if success, else False
        """
        return self.write_posts(
            posts=[post]
        )

    @abstractmethod
    def _get_bins(self, posts: List[Post]) -> Dict:
        """
        Get bins to save in Aerospike
        :param posts: list posts
        :return: bins as dict
        """
        pass

    def write_posts(self, posts: List[Post]) -> bool:
        """
        Write list of posts
        :param posts: posts to write
        :return: True if success, else False
        """
        try:
            bins = self._get_bins(posts=posts)
            client: Optional[Client] = self.connector.get_client()
            if client is None:
                return False
            client.put(
                key=self.key, meta={"ttl": self.time_to_live}, bins=bins
            )
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing posts to Aerospike"
            )
            return False


class BaseAerospikePostWriterVersion1Config(BasePostWriterConfig, ABC):
    """
    Write posts to Aerospike
    All posts will be saved in a pre-defined key
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            key: Tuple[str, str, str], time_to_live: int
    ):
        """
        Init method
        :param connector_config: connection to Aerospike
        :param key: key in Aerospike to store posts
        :param time_to_live: time to live in Aerospike
        """
        super(BaseAerospikePostWriterVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.key = key
        self.time_to_live = time_to_live

    @property
    def connector_config(self) -> BaseAerospikeConnectorProxyConfig:
        return self._connector_config

    @connector_config.setter
    def connector_config(self, connector_config: BaseAerospikeConnectorProxyConfig):
        assert isinstance(connector_config, BaseAerospikeConnectorProxyConfig)
        self._connector_config: BaseAerospikeConnectorProxyConfig = connector_config

    @property
    def key(self) -> Tuple[str, str, str]:
        return self._key

    @key.setter
    def key(self, key: Tuple[str, str, str]):
        assert isinstance(key, tuple)
        assert len(key) == 3
        assert all(map(lambda x: isinstance(x, str),
                       key))
        self._key: Tuple[str, str, str] = key

    @property
    def time_to_live(self) -> int:
        return self._time_to_live

    @time_to_live.setter
    def time_to_live(self, time_to_live: int):
        assert isinstance(time_to_live, int)
        self._time_to_live: int = time_to_live
