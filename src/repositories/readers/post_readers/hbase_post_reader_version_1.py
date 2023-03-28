from typing import List, Optional, Dict
from objects import Post, Encode
from .base_hbase_post_reader_version_1 import (
    BaseHbasePostReaderVersion1, BaseHbasePostReaderVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from logger import SingletonLogger
import pickle


class HbasePostReaderVersion1(BaseHbasePostReaderVersion1):
    """
    Read post's encodes from Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, encode_columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connector to Hbase
        :param table_name: name of table to read data
        :param encode_columns: columns to read encodes
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(HbasePostReaderVersion1, self).__init__(
            connector=connector, table_name=table_name,
            columns=encode_columns, batch_size=batch_size,
            verbose=verbose
        )
        self.encode_columns = encode_columns

    @property
    def encode_columns(self) -> List[bytes]:
        return self._encode_columns

    @encode_columns.setter
    def encode_columns(self, encode_columns: List[bytes]):
        assert isinstance(encode_columns, list)
        assert all(map(lambda x: isinstance(x, bytes), encode_columns))
        self._encode_columns: List[bytes] = encode_columns

    def _bytes_to_encode(self, data: bytes) -> Optional[Encode]:
        """
        Convert bytes to encode
        :param data: bytes data
        :return: encode object or None
        """
        try:
            data: object = pickle.loads(data)
            if not isinstance(data, dict):
                return None
            if not all(map(lambda x: x in data,
                           ["encode_name", "timestamp", "value"])):
                return None
            if not isinstance(data["encode_name"], str):
                return None
            if not isinstance(data["timestamp"], int):
                return None
            return Encode(
                encode_name=data["encode_name"], timestamp=data["timestamp"],
                value=data["value"]
            )
        except:
            SingletonLogger.get_instance().exception(
                "Exception while convert bytes to encode"
            )
            return None

    def _add_info_for_post(
            self, post: Post, row_dict: Dict[bytes, bytes]
    ):
        """
        Add info from row dict to post
        :param post: post to add info to
        :param row_dict: Hbase row dict
        """
        for column in self.encode_columns:
            if column not in row_dict:
                continue
            encode: Optional[Encode] = self._bytes_to_encode(
                data=row_dict[column]
            )
            if encode:
                post.add_encode(encode=encode)


class HbasePostReaderVersion1Config(BaseHbasePostReaderVersion1Config):
    """
    Config for Read post's encodes from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, encode_columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to Hbase
        :param table_name: name of table to read data
        :param encode_columns: columns to read encodes
        :param batch_size: batch size for reading posts
        :param verbose: display progress bar
        """
        super(HbasePostReaderVersion1Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, columns=encode_columns,
            batch_size=batch_size, verbose=verbose
        )
        self.encode_columns = encode_columns

    @property
    def encode_columns(self) -> List[bytes]:
        return self._encode_columns

    @encode_columns.setter
    def encode_columns(self, encode_columns: List[bytes]):
        assert isinstance(encode_columns, list)
        assert all(map(lambda x: isinstance(x, bytes), encode_columns))
        self._encode_columns: List[bytes] = encode_columns
