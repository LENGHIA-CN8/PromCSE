from typing import Optional, List, Tuple, Dict
from datetime import datetime
from objects import Post
from .base_hbase_relate_score_reader_version_1 import (
    BaseHbaseRelateScoreReaderVersion1,
    BaseHbaseRelateScoreReaderVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
import pickle
from logger import SingletonLogger


class HbaseRelateScoreReaderVersion1(BaseHbaseRelateScoreReaderVersion1):
    """
    Read relate recommend result from Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, column_name: bytes,
            batch_size: int, verbose: bool,
            stale_threshold: int
    ):
        """
        Init method
        :param connector: connection to database
        :param table_name: table that store result
        :param column_name: column that store result
        :param batch_size: batch size of training
        :param verbose: display progress bar
        :param stale_threshold: number of seconds that the result will be considered as stale
        """
        super(HbaseRelateScoreReaderVersion1, self).__init__(
            connector=connector, table_name=table_name,
            columns=[column_name], batch_size=batch_size,
            verbose=verbose
        )
        self.column_name = column_name
        self.stale_threshold = stale_threshold

    @property
    def column_name(self) -> bytes:
        return self._column_name

    @column_name.setter
    def column_name(self, column_name: bytes):
        assert isinstance(column_name, bytes)
        self._column_name: bytes = column_name

    @property
    def stale_threshold(self) -> int:
        return self._stale_threshold

    @stale_threshold.setter
    def stale_threshold(self, stale_threshold: int):
        assert isinstance(stale_threshold, int)
        self._stale_threshold: int = stale_threshold

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
        try:
            if self.column_name not in row_dict:
                return None
            data = pickle.loads(row_dict[self.column_name])
            if (
                not isinstance(data, dict) or
                not isinstance(data.get("timestamp"), int) or
                not isinstance(data.get("result"), list)
            ):
                return None
            current_timestamp: int = int(datetime.now().timestamp())
            if current_timestamp - data["timestamp"] > self.stale_threshold:
                return None
            posts_scores: List[Tuple[Post, float]] = []
            for post_id_score in data["result"]:
                if (
                    not isinstance(post_id_score, tuple) or
                    len(post_id_score) != 2 or
                    not isinstance(post_id_score[0], int) or
                    not isinstance(post_id_score[1], float)
                ):
                    continue
                posts_scores.append((
                    Post(post_id=post_id_score[0]),
                    post_id_score[1]
                ))
            return posts_scores
        except:
            SingletonLogger.get_instance().exception(
                "Exception while convert row dict to posts scores"
            )
            return None


class HbaseRelateScoreReaderVersion1Config(BaseHbaseRelateScoreReaderVersion1Config):
    """
    Config for read relate recommend result from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, column_name: bytes,
            batch_size: int, verbose: bool,
            stale_threshold: int
    ):
        """
        Init method
        :param connector_config: connection to database
        :param table_name: table that store result
        :param column_name: column that store result
        :param batch_size: batch size of training
        :param verbose: display progress bar
        :param stale_threshold: number of seconds that the result will be considered as stale
        """
        super(HbaseRelateScoreReaderVersion1Config, self).__init__(
            connector_config=connector_config, table_name=table_name,
            columns=[column_name], batch_size=batch_size,
            verbose=verbose
        )
        self.column_name = column_name
        self.stale_threshold = stale_threshold

    @property
    def column_name(self) -> bytes:
        return self._column_name

    @column_name.setter
    def column_name(self, column_name: bytes):
        assert isinstance(column_name, bytes)
        self._column_name: bytes = column_name

    @property
    def stale_threshold(self) -> int:
        return self._stale_threshold

    @stale_threshold.setter
    def stale_threshold(self, stale_threshold: int):
        assert isinstance(stale_threshold, int)
        self._stale_threshold: int = stale_threshold
