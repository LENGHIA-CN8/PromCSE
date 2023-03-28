from objects import Post
from .base_hbase_post_writer_version_1 import (
    BaseHbasePostWriterVersion1,
    BaseHbasePostWriterVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from typing import Dict


class HbasePostWriterVersion2(BaseHbasePostWriterVersion1):
    """
    Write post's tags to Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, tags_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connection to Hbase
        :param table_name: name of Hbase table
        :param tags_column: column to store tags
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(HbasePostWriterVersion2, self).__init__(
            connector=connector, table_name=table_name,
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

    def _post_to_row_dict(
            self, post: Post
    ) -> Dict[bytes, bytes]:
        """
        Convert post object to Hbase row dict
        :param post: post object to convert
        :return: dict mapping from column to value
        """
        if not post.tags:
            return {}
        else:
            return {
                self.tags_column: post.tags.encode("utf-8")
            }


class HbasePostWriterVersion2Config(BaseHbasePostWriterVersion1Config):
    """
    Config for write post's tags to Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, tags_column: bytes,
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to Hbase
        :param table_name: name of Hbase table
        :param tags_column: column to store tags
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(HbasePostWriterVersion2Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, batch_size=batch_size,
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
