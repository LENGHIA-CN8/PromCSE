from typing import Dict
from objects import Post
from .base_hbase_post_reader_version_1 import (
    BaseHbasePostReaderVersion1, BaseHbasePostReaderVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)


class HbasePostReaderVersion2(BaseHbasePostReaderVersion1):
    """
    Read post's tags from Hbase
    """

    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, tags_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connector to Hbase
        :param table_name: name of table to read data
        :param tags_column: column store tags
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(HbasePostReaderVersion2, self).__init__(
            connector=connector, table_name=table_name,
            columns=[tags_column], batch_size=batch_size,
            verbose=verbose
        )
        self.tags_column = tags_column

    @property
    def tags_column(self) -> bytes:
        return self._tags_column

    @tags_column.setter
    def tags_column(self, tags_column: bytes):
        assert isinstance(tags_column, bytes)
        self._tags_column: bytes = tags_column

    def _add_info_for_post(
            self, post: Post, row_dict: Dict[bytes, bytes]
    ):
        """
        Add info from row dict to post
        :param post: post to add info to
        :param row_dict: Hbase row dict
        """
        if self.tags_column in row_dict:
            post.tags = row_dict[self.tags_column].decode("utf-8")


class HbasePostReaderVersion2Config(BaseHbasePostReaderVersion1Config):
    """
    Config for Read post's tags from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, tags_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to Hbase
        :param table_name: name of table to read data
        :param tags_column: column store tags in Hbase
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(HbasePostReaderVersion2Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, columns=[tags_column],
            batch_size=batch_size, verbose=verbose
        )
        self.tags_column = tags_column

    @property
    def tags_column(self) -> bytes:
        return self._tags_column

    @tags_column.setter
    def tags_column(self, tags_column: bytes):
        assert isinstance(tags_column, bytes)
        self._tags_column: bytes = tags_column

