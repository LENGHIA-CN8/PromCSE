from typing import Optional, Dict, Tuple
from logger import SingletonLogger
from objects import Post
from .base_general_score_reader import (
    BaseGeneralScoreReader, BaseGeneralScoreReaderConfig
)
from connector_proxies import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from aerospike import Client
from abc import ABC, abstractmethod


class BaseAerospikeGeneralScoreReaderVersion1(BaseGeneralScoreReader, ABC):
    """
    Read general score from Aerospike
    """
    def __init__(
            self, connector: BaseAerospikeConnectorProxy,
            key: Tuple[str, str, str]
    ):
        """
        Init method
        :param connector: connection to Ae
        :param key: key in Ae store data
        """
        super(BaseAerospikeGeneralScoreReaderVersion1, self).__init__()
        self.connector = connector
        self.key = key

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

    @abstractmethod
    def _convert_bins_to_score(
            self, bins: Dict
    ) -> Optional[Dict[Post, float]]:
        """
        Convert AE bins to score
        :return: mapping from post to score, or None
        """
        pass

    def read(self) -> Optional[Dict[Post, float]]:
        """
        Read general score
        :return: mapping from post to score, or None if failed
        """
        try:
            client: Optional[Client] = self.connector.get_client()
            if client is None:
                return None
            _, meta = client.exists(self.key)
            if meta is None:
                return None
            _, _, bins = client.get(self.key)
            return self._convert_bins_to_score(bins=bins)
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading general score from Aerospike"
            )
            return None


class BaseAerospikeGeneralScoreReaderVersion1Config(BaseGeneralScoreReaderConfig, ABC):
    """
    Config for read general score from Aerospike
    """
    def __init__(
            self, connector_config: BaseAerospikeConnectorProxyConfig,
            key: Tuple[str, str, str]
    ):
        """
        Init method
        :param connector_config: connection to Ae
        :param key: key in Ae store data
        """
        super(BaseAerospikeGeneralScoreReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.key = key

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
