from objects import Post
from .base_post_writer import (
    BasePostWriter, BasePostWriterConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from typing import Dict, List
from logger import SingletonLogger
from happybase import Table
from tqdm import tqdm
from abc import ABC, abstractmethod


class BaseHbasePostWriterVersion1(BasePostWriter, ABC):
    """
    Base class for write post info to Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connection to Hbase
        :param table_name: name of Hbase table
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(BaseHbasePostWriterVersion1, self).__init__()
        self.connector = connector
        self.table_name = table_name
        self.batch_size = batch_size
        self.verbose = verbose

    @property
    def connector(self) -> BaseHbaseConnectorProxy:
        return self._connector

    @connector.setter
    def connector(self, connector: BaseHbaseConnectorProxy):
        assert isinstance(connector, BaseHbaseConnectorProxy)
        self._connector: BaseHbaseConnectorProxy = connector

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, table_name: str):
        assert isinstance(table_name, str)
        self._table_name: str = table_name

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

    def _gen_key(self, post: Post) -> bytes:
        """
        Gen row key for post
        :param post: post to gen key
        :return: hbase key
        """
        mode: int = post.post_id % 1000
        key: str = f"{mode:03d}_{post.post_id}"
        return key.encode("utf-8")

    @abstractmethod
    def _post_to_row_dict(
            self, post: Post
    ) -> Dict[bytes, bytes]:
        """
        Convert post object to Hbase row dict
        :param post: post object to convert
        :return: dict mapping from column to value
        """
        pass

    def write_post(self, post: Post) -> bool:
        """
        Write a post
        :param post: post to write
        :return: True if success, else False
        """
        try:
            row_key: bytes = self._gen_key(post=post)
            row_dict: Dict[bytes, bytes] = self._post_to_row_dict(
                post=post
            )
            with self.connector.get_connection() as connection:
                if connection is None:
                    return False
                table: Table = connection.table(self.table_name)
                table.put(row=row_key, data=row_dict)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing post to Hbase"
            )
            return False

    def write_posts(self, posts: List[Post]) -> bool:
        """
        Write list of posts
        :param posts: posts to write
        :return: True if success, else False
        """
        try:
            with self.connector.get_connection() as connection:
                if connection is None:
                    return False
                table: Table = connection.table(self.table_name)
                with table.batch(batch_size=self.batch_size) as batch:
                    if self.verbose:
                        progress_bar = tqdm(
                            iterable=posts,
                            desc="Writing posts to Hbase..."
                        )
                        for post in progress_bar:
                            row_key: bytes = self._gen_key(post=post)
                            row_dict: Dict[bytes, bytes] = self._post_to_row_dict(
                                post=post
                            )
                            batch.put(row=row_key, data=row_dict)
                        progress_bar.close()
                    else:
                        for post in posts:
                            row_key: bytes = self._gen_key(post=post)
                            row_dict: Dict[bytes, bytes] = self._post_to_row_dict(
                                post=post
                            )
                            batch.put(row=row_key, data=row_dict)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing posts to Hbase"
            )
            return False


class BaseHbasePostWriterVersion1Config(BasePostWriterConfig, ABC):
    """
    Config for write post info to Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to Hbase
        :param table_name: name of Hbase table
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(BaseHbasePostWriterVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.table_name = table_name
        self.batch_size = batch_size
        self.verbose = verbose

    @property
    def connector_config(self) -> BaseHbaseConnectorProxyConfig:
        return self._connector_config

    @connector_config.setter
    def connector_config(self, connector_config: BaseHbaseConnectorProxyConfig):
        assert isinstance(connector_config, BaseHbaseConnectorProxyConfig)
        self._connector_config: BaseHbaseConnectorProxyConfig = connector_config

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, table_name: str):
        assert isinstance(table_name, str)
        self._table_name: str = table_name

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

