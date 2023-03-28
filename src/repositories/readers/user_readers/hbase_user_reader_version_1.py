from typing import List, Optional, Dict
from objects import User, Post
from .base_user_reader import (
    BaseUserReader, BaseUserReaderConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from happybase import Table
from logger import SingletonLogger
import json
from tqdm import tqdm


class HbaseUserReaderVersion1(BaseUserReader):
    """
    Reading user positive, negative history from Hbase
    Only read id of posts in the history
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, batch_size: int,
            positive_column: bytes, negative_column: bytes,
            verbose: bool
    ):
        """
        Init method
        :param connector: connection to Hbase
        :param table_name: name of table
        :param batch_size: batch size of reading
        :param positive_column: column store positive history
        :param negative_column: column store negative history
        :param verbose: display progress bar
        """
        super(HbaseUserReaderVersion1, self).__init__()
        self.connector = connector
        self.table_name = table_name
        self.batch_size = batch_size
        self.positive_column = positive_column
        self.negative_column = negative_column
        self.verbose = verbose

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
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

    @property
    def positive_column(self) -> bytes:
        return self._positive_column

    @positive_column.setter
    def positive_column(self, positive_column: bytes):
        assert isinstance(positive_column, bytes)
        self._positive_column: bytes = positive_column

    @property
    def negative_column(self) -> bytes:
        return self._negative_column

    @negative_column.setter
    def negative_column(self, negative_column: bytes):
        assert isinstance(negative_column, bytes)
        self._negative_column: bytes = negative_column

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

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

    def _bytes_to_posts(self, data: bytes) -> Optional[List[Post]]:
        """
        Convert bytes to list of posts
        :param data: data to convert
        :return: list of posts, or None if failed
        """
        try:
            data: str = data.decode("utf-8")
            data = json.loads(data)
            if (
                not isinstance(data, list) or
                not all(map(lambda x: isinstance(x, int),
                            data))
            ):
                return None
            return [
                Post(post_id=post_id) for post_id in data
            ]
        except:
            SingletonLogger.get_instance().exception(
                "Exception while convert bytes to posts"
            )
            return None

    def read_user(self, user: User) -> bool:
        """
        Read user info
        :param user: user to read info
        :return: True if success, else False
        """
        try:
            key: bytes = self._gen_key(user=user)
            with self.connector.get_connection() as connection:
                if connection is None:
                    # can not get Hbase connection
                    return False
                table: Table = connection.table(self.table_name)
                row_dict: Optional[Dict[bytes, bytes]] = table.row(
                    row=key,
                    columns=[self.positive_column, self.negative_column]
                )
                if row_dict is None:
                    # no data
                    return True
                if self.positive_column in row_dict:
                    posts: Optional[List[Post]] = self._bytes_to_posts(
                        data=row_dict[self.positive_column]
                    )
                    if posts:
                        user.add_positive_posts(posts=posts)
                if self.negative_column in row_dict:
                    posts: Optional[List[Post]] = self._bytes_to_posts(
                        data=row_dict[self.negative_column]
                    )
                    if posts:
                        user.add_negative_posts(posts=posts)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading user info from Hbase"
            )
            return False

    def _read_users(self, users: List[User]) -> bool:
        """
        Read list users info
        :param users: list users to read info
        :return: True if success, else False
        """
        try:
            keys: List[bytes] = [
                self._gen_key(user=user) for user in users
            ]
            with self.connector.get_connection() as connection:
                if connection is None:
                    # can not get Hbase connection
                    return False
                table: Table = connection.table(self.table_name)
                user_to_query_user: Dict[User, User] = {}
                for row_key, row_dict in table.rows(
                    rows=keys,
                    columns=[self.positive_column, self.negative_column]
                ):
                    query_user: Optional[User] = self._parse_key(
                        key=row_key
                    )
                    if query_user is None:
                        continue
                    if self.positive_column in row_dict:
                        posts: Optional[List[Post]] = self._bytes_to_posts(
                            data=row_dict[self.positive_column]
                        )
                        if posts:
                            query_user.add_positive_posts(posts=posts)
                    if self.negative_column in row_dict:
                        posts: Optional[List[Post]] = self._bytes_to_posts(
                            data=row_dict[self.negative_column]
                        )
                        if posts:
                            query_user.add_negative_posts(posts=posts)
                    user_to_query_user[query_user] = query_user
            for user in users:
                user.update(other=user_to_query_user.get(user))
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading users info from Hbase"
            )
            return False

    def read_users(self, users: List[User]) -> bool:
        """
        Read list users info
        :param users: list users to read info
        :return: True if success, else False
        """
        if self.verbose:
            status: bool = True
            progress_bar = tqdm(
                iterable=range(0, len(users), self.batch_size),
                desc="Reading users history..."
            )
            for start_idx in progress_bar:
                end_idx: int = min(start_idx + self.batch_size, len(users))
                status = self._read_users(
                    users=users[start_idx:end_idx]
                ) and status
            progress_bar.close()
            return status
        else:
            status: bool = True
            for start_idx in range(0, len(users), self.batch_size):
                end_idx: int = min(start_idx + self.batch_size, len(users))
                status = self._read_users(
                    users=users[start_idx:end_idx]
                ) and status
            return status


class HbaseUserReaderVersion1Config(BaseUserReaderConfig):
    """
    Config for reading user positive, negative history from Hbase
    Only read id of posts in the history
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, batch_size: int,
            positive_column: bytes, negative_column: bytes,
            verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to Hbase
        :param table_name: name of table
        :param batch_size: batch size of reading
        :param positive_column: column store positive history
        :param negative_column: column store negative history
        :param verbose: display progress bar
        """
        super(HbaseUserReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.table_name = table_name
        self.batch_size = batch_size
        self.positive_column = positive_column
        self.negative_column = negative_column
        self.verbose = verbose

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
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

    @property
    def positive_column(self) -> bytes:
        return self._positive_column

    @positive_column.setter
    def positive_column(self, positive_column: bytes):
        assert isinstance(positive_column, bytes)
        self._positive_column: bytes = positive_column

    @property
    def negative_column(self) -> bytes:
        return self._negative_column

    @negative_column.setter
    def negative_column(self, negative_column: bytes):
        assert isinstance(negative_column, bytes)
        self._negative_column: bytes = negative_column

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose
