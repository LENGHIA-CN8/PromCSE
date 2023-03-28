from typing import List, Optional, Dict
from objects import Post
from .base_post_reader import (
    BasePostReader, BasePostReaderConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from logger import SingletonLogger
from happybase import Table
from tqdm import tqdm
from abc import abstractmethod, ABC


class BaseHbasePostReaderVersion1(BasePostReader, ABC):
    """
    Base class for reading posts info from Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connector to Hbase
        :param table_name: name of table to read data
        :param columns: columns to read data
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(BaseHbasePostReaderVersion1, self).__init__()
        self.connector = connector
        self.table_name = table_name
        self.columns = columns
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
    def columns(self) -> List[bytes]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[bytes]):
        assert isinstance(columns, list)
        assert all(map(lambda x: isinstance(x, bytes), columns))
        self._columns: List[bytes] = columns

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

    def _parse_key(self, key: bytes) -> Optional[Post]:
        """
        Parse row key
        :param key: key to parse
        :return: post or None
        """
        try:
            key: str = key.decode("utf-8")
            post_id: str = key[4:]
            if post_id.isnumeric():
                return Post(post_id=int(post_id))
            else:
                return None
        except:
            SingletonLogger.get_instance().exception(
                "Exception while parsing hbase row key"
            )
            return None

    @abstractmethod
    def _add_info_for_post(
            self, post: Post, row_dict: Dict[bytes, bytes]
    ):
        """
        Add info from row dict to post
        :param post: post to add info to
        :param row_dict: Hbase row dict
        """
        pass

    def read_post(self, post: Post) -> bool:
        """
        Read info of a post
        :param post: post to read info
        :return: True if success, else False
        """
        try:
            key: bytes = self._gen_key(post=post)
            with self.connector.get_connection() as connection:
                if connection is None:
                    return False
                table: Table = connection.table(self.table_name)
                row_dict: Optional[Dict[bytes, bytes]] = table.row(
                    row=key, columns=self.columns
                )
                if row_dict:
                    self._add_info_for_post(
                        post=post, row_dict=row_dict
                    )
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading post info from Hbase"
            )
            return False

    def _read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        try:
            keys: List[bytes] = [
                self._gen_key(post=post) for post in posts
            ]
            with self.connector.get_connection() as connection:
                if connection is None:
                    return False
                table: Table = connection.table(self.table_name)
                post_to_query_post: Dict[Post, Post] = {}
                for row_key, row_dict in table.rows(
                        rows=keys, columns=self.columns
                ):
                    query_post: Optional[Post] = self._parse_key(key=row_key)
                    if query_post is None:
                        continue
                    if row_dict:
                        self._add_info_for_post(
                            post=query_post, row_dict=row_dict
                        )
                        post_to_query_post[query_post] = query_post
            for post in posts:
                post.update(other=post_to_query_post.get(post))
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading posts info from Hbase"
            )
            return False

    def read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        if self.verbose:
            status: bool = True
            progress_bar = tqdm(
                iterable=range(0, len(posts), self.batch_size),
                desc="Reading posts info..."
            )
            for start_idx in progress_bar:
                end_idx: int = min(start_idx + self.batch_size, len(posts))
                status = self._read_posts(
                    posts=posts[start_idx:end_idx]
                ) and status
            progress_bar.close()
            return status
        else:
            status: bool = True
            for start_idx in range(0, len(posts), self.batch_size):
                end_idx: int = min(start_idx + self.batch_size, len(posts))
                status = self._read_posts(
                    posts=posts[start_idx:end_idx]
                ) and status
            return status


class BaseHbasePostReaderVersion1Config(BasePostReaderConfig, ABC):
    """
    Base config class for reading post info from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to Hbase
        :param table_name: name of table to read data
        :param columns: columns to read info
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(BaseHbasePostReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.table_name = table_name
        self.columns = columns
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
    def columns(self) -> List[bytes]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[bytes]):
        assert isinstance(columns, list)
        assert all(map(lambda x: isinstance(x, bytes), columns))
        self._columns: List[bytes] = columns

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
