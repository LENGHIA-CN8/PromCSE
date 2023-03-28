from typing import Dict
from objects import Post
from .base_hbase_post_reader_version_1 import (
    BaseHbasePostReaderVersion1, BaseHbasePostReaderVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)


class HbasePostReaderVersion3(BaseHbasePostReaderVersion1):
    """
    Read post's ners from Hbase
    """

    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, ners_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connector to Hbase
        :param table_name: name of table to read data
        :param ners_column: column store ners
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(HbasePostReaderVersion3, self).__init__(
            connector=connector, table_name=table_name,
            columns=[ners_column], batch_size=batch_size,
            verbose=verbose
        )
        self.ners_column = ners_column

    @property
    def ners_column(self) -> bytes:
        return self._ners_column

    @ners_column.setter
    def ners_column(self, ners_column: bytes):
        assert isinstance(ners_column, bytes)
        self._ners_column: bytes = ners_column

    def _add_info_for_post(
            self, post: Post, row_dict: Dict[bytes, bytes]
    ):
        """
        Add info from row dict to post
        :param post: post to add info to
        :param row_dict: Hbase row dict
        """
        if self.ners_column in row_dict:
            post.ners = row_dict[self.ners_column].decode("utf-8")


class HbasePostReaderVersion3Config(BaseHbasePostReaderVersion1Config):
    """
    Config for Read post's ners from Hbase
    """

    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, ners_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to Hbase
        :param table_name: name of table to read data
        :param ners_column: column store ners in Hbase
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(HbasePostReaderVersion3Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, columns=[ners_column],
            batch_size=batch_size, verbose=verbose
        )
        self.ners_column = ners_column

    @property
    def ners_column(self) -> bytes:
        return self._ners_column

    @ners_column.setter
    def ners_column(self, ners_column: bytes):
        assert isinstance(ners_column, bytes)
        self._ners_column: bytes = ners_column
