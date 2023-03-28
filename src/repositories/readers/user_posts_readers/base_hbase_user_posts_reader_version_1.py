from logger import SingletonLogger
from objects import User, Post
from .base_user_posts_reader import (
    BaseUserPostsReader, BaseUserPostsReaderConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from happybase import Table


class BaseHbaseUserPostsReaderVersion1(BaseUserPostsReader, ABC):
    """
    Read user posts from Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, columns: List[bytes]
    ):
        """
        Init method
        :param connector: connector to Hbase
        :param table_name: name of table to read
        :param columns: list of columns to read
        """
        super(BaseHbaseUserPostsReaderVersion1, self).__init__()
        self.connector = connector
        self.table_name = table_name
        self.columns = columns

    @property
    def connector(self) -> BaseHbaseConnectorProxy:
        return self._connector

    @connector.setter
    def connector(self, connector: BaseHbaseConnectorProxy):
        assert isinstance(connector, BaseHbaseConnectorProxy)
        self._connector: BaseHbaseConnectorProxy = connector

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, table_name: str):
        assert isinstance(table_name, str)
        self._table_name: str = table_name

    @property
    def columns(self) -> List[bytes]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[bytes]):
        assert isinstance(columns, list)
        assert all(map(lambda x: isinstance(x, bytes), columns))
        self._columns: List[bytes] = columns

    def _gen_key(self, user: User) -> bytes:
        """
        Gen Hbase key for user
        :param user: user to gen key
        :return: key as bytes
        """
        user_id: int = user.user_id
        mode: int = user_id % 1000
        key: str = f"{mode:03d}_{user_id}"
        return key.encode("utf-8")

    def _parse_key(self, key: bytes) -> Optional[User]:
        """
        Convert Hbase key to user
        :param key: Hbase key to parse
        :return: user if success, else  None
        """
        key: str = key.decode("utf-8")
        user_id_str: str = key[4:]
        if user_id_str.isdigit():
            return User(user_id=int(user_id_str))
        else:
            return None

    @abstractmethod
    def _convert_row_dict_to_posts(
            self, row_dict: Dict[bytes, bytes]
    ) -> Optional[List[Post]]:
        """
        Convert hbase row dict to posts
        :param row_dict: hbase row dict
        :return: list of posts or None
        """
        pass

    def read_user(
            self, user: User
    ) -> Optional[List[Post]]:
        """
        Read list posts related to user
        :param user: user to read
        :return: list posts related to user, or None
        """
        try:
            key: bytes = self._gen_key(user=user)
            with self.connector.get_connection() as connection:
                if connection is None:
                    return None
                table: Table = connection.table(self.table_name)
                row_dict: Optional[
                    Dict[bytes, bytes]
                ] = table.row(
                    row=key, columns=self.columns
                )
                if row_dict is None:
                    return None
                return self._convert_row_dict_to_posts(
                    row_dict=row_dict
                )
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading user posts from Hbase"
            )
            return None


class BaseHbaseUserPostsReaderVersion1Config(BaseUserPostsReaderConfig, ABC):
    """
    Read user posts from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, columns: List[bytes]
    ):
        """
        Init method
        :param connector_config: connector to Hbase
        :param table_name: name of table to read
        :param columns: list of columns to read
        """
        super(BaseHbaseUserPostsReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.table_name = table_name
        self.columns = columns

    @property
    def connector_config(self) -> BaseHbaseConnectorProxyConfig:
        return self._connector_config

    @connector_config.setter
    def connector_config(self, connector_config: BaseHbaseConnectorProxyConfig):
        assert isinstance(connector_config, BaseHbaseConnectorProxyConfig)
        self._connector_config: BaseHbaseConnectorProxyConfig = connector_config

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, table_name: str):
        assert isinstance(table_name, str)
        self._table_name: str = table_name

    @property
    def columns(self) -> List[bytes]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[bytes]):
        assert isinstance(columns, list)
        assert all(map(lambda x: isinstance(x, bytes), columns))
        self._columns: List[bytes] = columns
