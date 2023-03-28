from typing import Optional, List, Tuple, Dict
from objects import Post
from .base_relate_score_reader import (
    BaseRelateScoreReader, BaseRelateScoreReaderConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from logger import SingletonLogger
from happybase import Table
from tqdm import tqdm
from abc import ABC, abstractmethod


class BaseHbaseRelateScoreReaderVersion1(BaseRelateScoreReader, ABC):
    """
    Read relate recommend result from Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connection to database
        :param table_name: table that store result
        :param columns: list columns to read
        :param batch_size: batch size of training
        :param verbose: display progress bar
        """
        super(BaseHbaseRelateScoreReaderVersion1, self).__init__()
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
        Gen Hbase key for post
        :param post: post to gen key
        :return: key as bytes
        """
        post_id: int = post.post_id
        mode: int = post_id % 1000
        key: str = f"{mode:03d}_{post_id}"
        return key.encode("utf-8")

    def _parse_key(self, key: bytes) -> Optional[Post]:
        """
        Convert Hbase key to post
        :param key: Hbase key to parse
        :return: post if success, else  None
        """
        key: str = key.decode("utf-8")
        post_id_str: str = key[4:]
        if post_id_str.isdigit():
            return Post(post_id=int(post_id_str))
        else:
            return None

    @abstractmethod
    def _row_dict_to_posts_scores(
            self, row_dict: Dict[bytes, bytes]
    ) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Convert bytes to posts scores
        :param row_dict: hbase row dict
        :return: list of (post, score); or None
        """
        pass

    def read_post(self, post: Post) -> Optional[
        List[
            Tuple[Post, float]
        ]
    ]:
        """
        Read relate score for a post
        :return: list of (post, score) or None
        """
        try:
            key: bytes = self._gen_key(post=post)
            with self.connector.get_connection() as connection:
                if connection is None:
                    return None
                table: Table = connection.table(self.table_name)
                row_dict: Optional[
                    Dict[bytes, bytes]
                ] = table.row(row=key, columns=self.columns)
                if row_dict is None:
                    return None
                return self._row_dict_to_posts_scores(row_dict=row_dict)
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading relate score from Hbase"
            )
            return None

    def _read_posts(self, posts: List[Post]) -> Optional[
        Dict[
            Post,
            List[Tuple[Post, float]]
        ]
    ]:
        """
        Read relate score for list of posts
        :return: mapping from post to list of (post, score); or None
        """
        try:
            post_to_result: Dict[
                Post,
                List[Tuple[Post, float]]
            ] = {}
            keys: List[bytes] = [
                self._gen_key(post=post) for post in posts
            ]
            with self.connector.get_connection() as connection:
                if connection is None:
                    return None
                table: Table = connection.table(self.table_name)
                for row_key, row_dict in table.rows(
                    rows=keys, columns=self.columns
                ):
                    post: Optional[Post] = self._parse_key(key=row_key)
                    if (
                            post is None or
                            row_dict is None
                    ):
                        continue
                    posts_scores: Optional[
                        List[Tuple[Post, float]]
                    ] = self._row_dict_to_posts_scores(row_dict=row_dict)
                    if posts_scores:
                        post_to_result[post] = posts_scores
            return post_to_result
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading relate scores from Hbase"
            )
            return None

    def read_posts(self, posts: List[Post]) -> Optional[
        Dict[
            Post,
            List[Tuple[Post, float]]
        ]
    ]:
        """
        Read relate score for list of posts
        :return: mapping from post to list of (post, score); or None
        """
        post_to_result: Dict[
            Post,
            List[Tuple[Post, float]]
        ] = {}
        if self.verbose:
            progress_bar = tqdm(
                iterable=range(0, len(posts), self.batch_size),
                desc="Reading relate results..."
            )
            for start_idx in progress_bar:
                end_idx: int = min(start_idx + self.batch_size, len(posts))
                data: Optional[
                    Dict[
                        Post,
                        List[Tuple[Post, float]]
                    ]
                ] = self._read_posts(posts=posts[start_idx:end_idx])
                if data:
                    post_to_result.update(data)
            progress_bar.close()
            return post_to_result
        else:
            for start_idx in range(0, len(posts), self.batch_size):
                end_idx: int = min(start_idx + self.batch_size, len(posts))
                data: Optional[
                    Dict[
                        Post,
                        List[Tuple[Post, float]]
                    ]
                ] = self._read_posts(posts=posts[start_idx:end_idx])
                if data:
                    post_to_result.update(data)
            return post_to_result


class BaseHbaseRelateScoreReaderVersion1Config(BaseRelateScoreReaderConfig, ABC):
    """
    Config for read relate recommend result from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to database
        :param table_name: table that store result
        :param batch_size: batch size of training
        :param verbose: display progress bar
        """
        super(BaseHbaseRelateScoreReaderVersion1Config, self).__init__()
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
