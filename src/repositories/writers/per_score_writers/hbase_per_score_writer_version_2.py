from typing import List, Tuple, Dict
from objects import Post
from .base_hbase_per_score_writer_version_1 import (
    BaseHbasePerScoreWriterVersion1Config,
    BaseHbasePerScoreWriterVersion1
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
import pickle
from datetime import datetime


class HbasePerScoreWriterVersion2(BaseHbasePerScoreWriterVersion1):
    """
    Write per score to Hbase, only saving post_id of candidates
    Also save timestamp of write operation
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, column: bytes, batch_size: int,
            verbose: bool
    ):
        """
        Init method
        :param connector: connector to Database
        :param table_name: name of the table
        :param column: name of column store recommend result
        :param batch_size: batch size of writing
        :param verbose: display progress bar
        """
        super(HbasePerScoreWriterVersion2, self).__init__(
            connector=connector, table_name=table_name,
            batch_size=batch_size, verbose=verbose
        )
        self.column = column

    @property
    def column(self) -> bytes:
        return self._column

    @column.setter
    def column(self, column: bytes):
        assert isinstance(column, bytes)
        self._column: bytes = column

    def _posts_scores_to_row_dict(
            self, posts_scores: List[Tuple[Post, float]]
    ) -> Dict[bytes, bytes]:
        """
        Convert list of (post, score) to row dict to save in Hbase
        :param posts_scores: list of tuple (post, score)
        :return: row dict
        """
        data: List[Tuple[int, float]] = [
            (post.post_id, score)
            for post, score in posts_scores
        ]
        data: Dict = {
            "timestamp": int(datetime.now().timestamp()),
            "result": data
        }
        data: bytes = pickle.dumps(data)
        return {
            self.column: data
        }


class HbasePerScoreWriterVersion2Config(BaseHbasePerScoreWriterVersion1Config):
    """
    Config for write per score to Hbase, only saving post_id of candidates
    Also save timestamp of write operation
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, column: bytes, batch_size: int,
            verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to Database
        :param table_name: name of the table
        :param column: name of column store recommend result
        :param batch_size: batch size of writing
        :param verbose: display progress bar
        """
        super(HbasePerScoreWriterVersion2Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, batch_size=batch_size,
            verbose=verbose
        )
        self.column = column

    @property
    def column(self) -> bytes:
        return self._column

    @column.setter
    def column(self, column: bytes):
        assert isinstance(column, bytes)
        self._column: bytes = column
