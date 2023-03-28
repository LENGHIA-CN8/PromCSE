from typing import List, Tuple, Dict
from objects import Post
from .base_hbase_relate_score_writer_version_1 import (
    BaseHbaseRelateScoreWriterVersion1,
    BaseHbaseRelateScoreWriterVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
import pickle


class HbaseRelateScoreWriterVersion1(BaseHbaseRelateScoreWriterVersion1):
    """
    Write relate score to Hbase, only saving post_id of candidates
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
        super(HbaseRelateScoreWriterVersion1, self).__init__(
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
        data: bytes = pickle.dumps(data)
        return {
            self.column: data
        }


class HbaseRelateScoreWriterVersion1Config(BaseHbaseRelateScoreWriterVersion1Config):
    """
    Config for write relate score to Hbase, only saving post_id of candidates
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
        super(HbaseRelateScoreWriterVersion1Config, self).__init__(
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
