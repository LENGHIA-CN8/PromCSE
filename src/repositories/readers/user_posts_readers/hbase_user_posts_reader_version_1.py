from typing import Dict, Optional, List
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from objects import Post
from .base_hbase_user_posts_reader_version_1 import (
    BaseHbaseUserPostsReaderVersion1, BaseHbaseUserPostsReaderVersion1Config
)
import json
from logger import SingletonLogger


class HbaseUserPostsReaderVersion1(BaseHbaseUserPostsReaderVersion1):
    """
    Read posts from a column
    Column save post ids as list
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, column: bytes
    ):
        """
        Init method
        :param connector: connector to Hbase
        :param table_name: name of table to read
        :param column: column to read
        """
        super(HbaseUserPostsReaderVersion1, self).__init__(
            connector=connector, table_name=table_name,
            columns=[column]
        )
        self.column = column

    @property
    def column(self) -> bytes:
        return self._column

    @column.setter
    def column(self, column: bytes):
        assert isinstance(column, bytes)
        self._column: bytes = column

    def _convert_row_dict_to_posts(
            self, row_dict: Dict[bytes, bytes]
    ) -> Optional[List[Post]]:
        """
        Convert hbase row dict to posts
        :param row_dict: hbase row dict
        :return: list of posts or None
        """
        try:
            if self.column not in row_dict:
                return None
            data = json.loads(
                row_dict[self.column].decode("utf-8")
            )
            if not isinstance(data, list):
                return None
            return list(
                set([
                    Post(post_id=post_id)
                    for post_id in data if isinstance(post_id, int)
                ])
            )
        except:
            SingletonLogger.get_instance().exception(
                "Exception while convert bytes to posts"
            )
            return None


class HbaseUserPostsReaderVersion1Config(BaseHbaseUserPostsReaderVersion1Config):
    """
    Read posts from a column
    Column save post ids as list
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, column: bytes
    ):
        """
        Init method
        :param connector_config: connector to Hbase
        :param table_name: name of table to read
        :param column: column to read
        """
        super(HbaseUserPostsReaderVersion1Config, self).__init__(
            connector_config=connector_config, table_name=table_name,
            columns=[column]
        )
        self.column = column

    @property
    def column(self) -> bytes:
        return self._column

    @column.setter
    def column(self, column: bytes):
        assert isinstance(column, bytes)
        self._column: bytes = column
