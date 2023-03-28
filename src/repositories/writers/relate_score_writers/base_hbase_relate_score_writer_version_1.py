from typing import List, Tuple, Dict
from logger import SingletonLogger
from objects import Post
from .base_relate_score_writer import (
    BaseRelateScoreWriter, BaseRelateScoreWriterConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from abc import ABC, abstractmethod
from happybase import Table
from tqdm import tqdm


class BaseHbaseRelateScoreWriterVersion1(BaseRelateScoreWriter, ABC):
    """
    Write relate score to Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connector to Database
        :param table_name: name of the table
        :param batch_size: batch size of writing
        :param verbose: display progress bar
        """
        super(BaseHbaseRelateScoreWriterVersion1, self).__init__()
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
    def _posts_scores_to_row_dict(
            self, posts_scores: List[Tuple[Post, float]]
    ) -> Dict[bytes, bytes]:
        """
        Convert list of (post, score) to row dict to save in Hbase
        :param posts_scores: list of tuple (post, score)
        :return: row dict
        """
        pass

    def write_score(
            self, seed_post: Post,
            posts_scores: List[Tuple[Post, float]]
    ) -> bool:
        """
        Write relate score
        :param seed_post: seed post
        :param posts_scores: list scores of candidates. list of tuple (post, score)
        :return: True if success, else False
        """
        try:
            key: bytes = self._gen_key(post=seed_post)
            row_dict: Dict[bytes, bytes] = self._posts_scores_to_row_dict(
                posts_scores=posts_scores
            )
            with self.connector.get_connection() as connection:
                if connection is None:
                    return False
                table: Table = connection.table(self.table_name)
                table.put(row=key, data=row_dict)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing relate result to Hbase"
            )
            return False

    def write_scores(
            self, seed_post_to_result: Dict[
                Post,
                List[Tuple[Post, float]]
            ]
    ) -> bool:
        """
        Write multiple relate scores
        :param seed_post_to_result: mapping from seed post to list of tuple (post, score)
        :return True if success, else False
        """
        try:
            with self.connector.get_connection() as connection:
                if connection is None:
                    return False
                table: Table = connection.table(self.table_name)
                with table.batch(batch_size=self.batch_size) as batch:
                    if self.verbose:
                        progress_bar = tqdm(
                            iterable=seed_post_to_result.items(),
                            desc="Writing relate score to Hbase..."
                        )
                        for seed_post, posts_scores in progress_bar:
                            key: bytes = self._gen_key(post=seed_post)
                            row_dict: Dict[bytes, bytes] = self._posts_scores_to_row_dict(
                                posts_scores=posts_scores
                            )
                            batch.put(row=key, data=row_dict)
                        progress_bar.close()
                    else:
                        for seed_post, posts_scores in seed_post_to_result.items():
                            key: bytes = self._gen_key(post=seed_post)
                            row_dict: Dict[bytes, bytes] = self._posts_scores_to_row_dict(
                                posts_scores=posts_scores
                            )
                            batch.put(row=key, data=row_dict)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing relate results to Hbase"
            )
            return False


class BaseHbaseRelateScoreWriterVersion1Config(BaseRelateScoreWriterConfig, ABC):
    """
    Config for write relate score to Hbase, only saving post_id of candidates
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to Database
        :param table_name: name of the table
        :param batch_size: batch size of writing
        :param verbose: display progress bar
        """
        super(BaseHbaseRelateScoreWriterVersion1Config, self).__init__()
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
