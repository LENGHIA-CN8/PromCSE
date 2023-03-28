from typing import Optional
from objects import Post, Encode
from .base_hbase_post_writer_version_1 import (
    BaseHbasePostWriterVersion1,
    BaseHbasePostWriterVersion1Config
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from typing import Dict
from torch import Tensor
import pickle


class HbasePostWriterVersion1(BaseHbasePostWriterVersion1):
    """
    Write post's encodes to Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, encode_name_to_column: Dict[str, bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connection to Hbase
        :param table_name: name of Hbase table
        :param encode_name_to_column: mapping from encode name to Hbase column
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(HbasePostWriterVersion1, self).__init__(
            connector=connector, table_name=table_name,
            batch_size=batch_size, verbose=verbose
        )
        self.encode_name_to_column = encode_name_to_column

    @property
    def encode_name_to_column(self) -> Dict[str, bytes]:
        return self._encode_name_to_column
    
    @encode_name_to_column.setter
    def encode_name_to_column(self, encode_name_to_column: Dict[str, bytes]):
        assert isinstance(encode_name_to_column, dict)
        assert all(map(lambda x: isinstance(x, str),
                       encode_name_to_column.keys()))
        assert all(map(lambda x: isinstance(x, bytes),
                       encode_name_to_column.values()))
        self._encode_name_to_column: Dict[str, bytes] = encode_name_to_column

    def _encode_to_bytes(self, encode: Encode) -> bytes:
        """
        Convert encode object to bytes
        :param encode: encode object
        :return: bytes data
        """
        data: Dict = {
            "encode_name": encode.encode_name,
            "timestamp": encode.timestamp,
            "value": encode.value.numpy() if isinstance(
                encode.value, Tensor
            ) else encode.value
        }
        return pickle.dumps(data)

    def _post_to_row_dict(self, post: Post) -> Dict[bytes, bytes]:
        """
        Convert post object to Hbase row dict
        :param post: post object to convert
        :return: dict mapping from column to value
        """
        row_dict: Dict[bytes, bytes] = {}
        for encode_name, column in self.encode_name_to_column.items():
            encode: Optional[Encode] = post.get_encode(
                encode_name=encode_name
            )
            if encode is not None:
                row_dict[column] = self._encode_to_bytes(
                    encode=encode
                )
        return row_dict


class HbasePostWriterVersion1Config(BaseHbasePostWriterVersion1Config):
    """
    Config for write post encode to Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, encode_name_to_column: Dict[str, bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to Hbase
        :param table_name: name of Hbase table
        :param encode_name_to_column: mapping from encode name to Hbase column
        :param batch_size: batch size of writing
        :param verbose: display progress bar while writing
        """
        super(HbasePostWriterVersion1Config, self).__init__(
            connector_config=connector_config,
            table_name=table_name, batch_size=batch_size,
            verbose=verbose
        )
        self.encode_name_to_column = encode_name_to_column

    @property
    def encode_name_to_column(self) -> Dict[str, bytes]:
        return self._encode_name_to_column

    @encode_name_to_column.setter
    def encode_name_to_column(self, encode_name_to_column: Dict[str, bytes]):
        assert isinstance(encode_name_to_column, dict)
        assert all(map(lambda x: isinstance(x, str),
                       encode_name_to_column.keys()))
        assert all(map(lambda x: isinstance(x, bytes),
                       encode_name_to_column.values()))
        self._encode_name_to_column: Dict[str, bytes] = encode_name_to_column
