from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Optional
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from objects import User, Post
from .base_user_posts_writer import (
    BaseUserPostsWriter, BaseUserPostsWriterConfig
)
from aerospike import Client
from logger import SingletonLogger


class BaseAerospikeUserPostsWriterVersion1(BaseUserPostsWriter, ABC):
    """
    Base class for writing user posts to Aerospike
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            ae_namespace: str, ae_set: str,
            time_to_live: int
    ):
        """
        Init method
        :param connector: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        :param time_to_live: time to persist data
        """
        super(BaseAerospikeUserPostsWriterVersion1, self).__init__()
        self.connector = connector
        self.ae_namespace = ae_namespace
        self.ae_set = ae_set
        self.time_to_live = time_to_live

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

    @property
    def time_to_live(self) -> int:
        return self._time_to_live

    @time_to_live.setter
    def time_to_live(self, time_to_live: int):
        assert isinstance(time_to_live, int)
        self._time_to_live: int = time_to_live

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
    def _convert_posts_to_bins(
            self, posts: List[Post], old_bins: Dict
    ) -> Dict:
        """
        Convert posts to bins
        :param posts: posts to convert
        :param old_bins: old bins data in Ae
        :return: new bins data
        """
        pass

    def write(
            self, user: User, posts: List[Post]
    ) -> bool:
        """
        Write user posts
        :param user: User
        :param posts: posts
        """
        try:
            key: Tuple[str, str, str] = self._gen_key(user=user)
            client: Optional[Client] = self.connector.get_client()
            if client is None:
                return False
            _, meta = client.exists(key)
            if meta is None:
                old_bins: Dict = {}
            else:
                _, _, old_bins = client.get(key)
            bins: Dict = self._convert_posts_to_bins(
                posts=posts, old_bins=old_bins
            )
            client.put(
                key=key, meta={"ttl": self.time_to_live}, bins=bins
            )
            return True
        except:
            SingletonLogger.get_instance().exception(
                f"Exception while writing user posts from Aerospike"
            )
            return False


class BaseAerospikeUserPostsWriterVersion1Config(BaseUserPostsWriterConfig, ABC):
    """
    Base config class for writing user posts to Aerospike
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            ae_namespace: str, ae_set: str,
            time_to_live: int
    ):
        """
        Init method
        :param connector_config: connector to AE
        :param ae_namespace: name space store data
        :param ae_set: set store data
        :param time_to_live: time to persist data
        """
        super(BaseAerospikeUserPostsWriterVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.ae_namespace = ae_namespace
        self.ae_set = ae_set
        self.time_to_live = time_to_live

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

    @property
    def time_to_live(self) -> int:
        return self._time_to_live

    @time_to_live.setter
    def time_to_live(self, time_to_live: int):
        assert isinstance(time_to_live, int)
        self._time_to_live: int = time_to_live
