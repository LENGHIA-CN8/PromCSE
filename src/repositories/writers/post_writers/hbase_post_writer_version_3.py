from objects import Post
from .base_hbase_post_writer_version_1 import (
    BaseHbasePostWriterVersion1,
    BaseHbasePostWriterVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from typing import Dict


class HbasePostWriterVersion3(BaseHbasePostWriterVersion1):
    """
    Write post's ners to Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, ners_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connection to Hbase
        :param table_name: name of Hbase table
        :param ners_column: column to store ners
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(HbasePostWriterVersion3, self).__init__(
            connector=connector, table_name=table_name,
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

    def _post_to_row_dict(
            self, post: Post
    ) -> Dict[bytes, bytes]:
        """
        Convert post object to Hbase row dict
        :param post: post object to convert
        :return: dict mapping from column to value
        """
        if not post.ners:
            return {}
        else:
            return {
                self.ners_column: post.ners.encode("utf-8")
            }


class HbasePostWriterVersion3Config(BaseHbasePostWriterVersion1Config):
    """
    Config for write post's ners to Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, ners_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to Hbase
        :param table_name: name of Hbase table
        :param ners_column: column to store ners
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(HbasePostWriterVersion3Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, batch_size=batch_size,
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
