from typing import Dict, Tuple, Optional
from aerospike import Client
from objects import Post
from .base_general_score_writer import (
    BaseGeneralScoreWriter, BaseGeneralScoreWriterConfig
)
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from logger import SingletonLogger
from abc import ABC, abstractmethod


class BaseAerospikeGeneralScoreWriterVersion1(BaseGeneralScoreWriter, ABC):
    """
    Class for writing general score to Aerospike
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            key: Tuple[str, str, str], time_to_live: int
    ):
        """
        Init method
        :param connector: connection to Aerospike
        :param key: key store data in Aerospike
        :param time_to_live: time to save result on Aerospike
        """
        super(BaseAerospikeGeneralScoreWriterVersion1, self).__init__()
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

    @abstractmethod
    def _get_bins(self, post_to_score: Dict[Post, float]) -> Dict:
        """
        Get bins to save in Aerospike
        :param post_to_score: mapping from post to score
        :return: bins as dict
        """
        pass

    def write(self, post_to_score: Dict[Post, float]) -> bool:
        """
        Write general score
        :param post_to_score: mapping from post to score
        :return: True if success, else False
        """
        try:
            bins = self._get_bins(post_to_score=post_to_score)
            client: Optional[Client] = self.connector.get_client()
            if not client:
                return False
            client.put(
                key=self.key, meta={"ttl": self.time_to_live}, bins=bins
            )
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing general score to Aerospike"
            )
            return False


class BaseAerospikeGeneralScoreWriterVersion1Config(BaseGeneralScoreWriterConfig, ABC):
    """
    Config class for writing general score to Aerospike
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            key: Tuple[str, str, str], time_to_live: int
    ):
        """
        Init method
        :param connector_config: connection to Aerospike
        :param key: key store data in Aerospike
        :param time_to_live: time to save result on Aerospike
        """
        super(BaseAerospikeGeneralScoreWriterVersion1Config, self).__init__()
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
