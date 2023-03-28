from typing import Optional, List
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from objects import User
from .base_all_users_reader import (
    BaseAllUsersReader, BaseAllUsersReaderConfig
)
from happybase import Table
from logger import SingletonLogger


class HbaseAllUsersReaderVersion1(BaseAllUsersReader):
    """
    Read users from Hbase
    Each call: scan all users with specific row_prefix
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, column: bytes
    ):
        """
        Init method
        :param connector: connection to database
        :param table_name: name of table
        :param column: column to scan
        """
        super(HbaseAllUsersReaderVersion1, self).__init__()
        self.connector = connector
        self.table_name = table_name
        self.column = column
        self._current_prefix: int = 0
        
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
    def column(self) -> bytes:
        return self._column

    @column.setter
    def column(self, column: bytes):
        assert isinstance(column, bytes)
        self._column: bytes = column

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

    def read_users(self) -> Optional[List[User]]:
        """
        Read list of users
        :return: list of users or None
        """
        try:
            with self.connector.get_connection() as connection:
                if connection is None:
                    return None
                table: Table = connection.table(self.table_name)
                row_prefix: str = f"{self._current_prefix:03d}"
                row_prefix: bytes = row_prefix.encode("utf-8")
                users: List[User] = []
                for row_key, _ in table.scan(
                    row_prefix=row_prefix, columns=[self.column]
                ):
                    user: Optional[User] = self._parse_key(
                        key=row_key
                    )
                    if user:
                        users.append(user)
                self._current_prefix += 1
                if self._current_prefix >= 1000:
                    self._current_prefix = 0
            return users
        except:
            SingletonLogger.get_instance().exception(
                "Exception while read users from Hbase"
            )
            return None


class HbaseAllUsersReaderVersion1Config(BaseAllUsersReaderConfig):
    """
    Config for read users from Hbase
    Each call: scan all users with specific row_prefix
    """

    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, column: bytes
    ):
        """
        Init method
        :param connector_config: connection to database
        :param table_name: name of table
        :param column: column to scan
        """
        super(HbaseAllUsersReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.table_name = table_name
        self.column = column

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
    def column(self) -> bytes:
        return self._column

    @column.setter
    def column(self, column: bytes):
        assert isinstance(column, bytes)
        self._column: bytes = column
