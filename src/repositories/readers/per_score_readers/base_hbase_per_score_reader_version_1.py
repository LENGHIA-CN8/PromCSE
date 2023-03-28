from typing import Optional, List, Tuple, Dict
from objects import User, Post
from .base_per_score_reader import (
    BasePerScoreReader, BasePerScoreReaderConfig
)
from connector_proxies import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from logger import SingletonLogger
from happybase import Table
from tqdm import tqdm
from abc import ABC, abstractmethod


class BaseHbasePerScoreReaderVersion1(BasePerScoreReader, ABC):
    """
    Read per recommend result from Hbase
    """
    def __init__(
            self, connector: BaseHbaseConnectorProxy,
            table_name: str, columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connection to database
        :param table_name: table that store result
        :param columns: list columns to read
        :param batch_size: batch size of training
        :param verbose: display progress bar
        """
        super(BaseHbasePerScoreReaderVersion1, self).__init__()
        self.connector = connector
        self.table_name = table_name
        self.columns = columns
        self.batch_size = batch_size
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
    def columns(self) -> List[bytes]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[bytes]):
        assert isinstance(columns, list)
        assert all(map(lambda x: isinstance(x, bytes), columns))
        self._columns: List[bytes] = columns

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

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

    @abstractmethod
    def _row_dict_to_posts_scores(
            self, row_dict: Dict[bytes, bytes]
    ) -> Optional[
        List[Tuple[Post, float]]
    ]:
        """
        Convert bytes to posts scores
        :param row_dict: hbase row dict
        :return: list of (post, score); or None
        """
        pass

    def read_user(self, user: User) -> Optional[
        List[
            Tuple[Post, float]
        ]
    ]:
        """
        Read per score for a user
        :return: list of (post, score) or None
        """
        try:
            key: bytes = self._gen_key(user=user)
            with self.connector.get_connection() as connection:
                if connection is None:
                    return None
                table: Table = connection.table(self.table_name)
                row_dict: Optional[
                    Dict[bytes, bytes]
                ] = table.row(row=key, columns=self.columns)
                if row_dict is None:
                    return None
                return self._row_dict_to_posts_scores(row_dict=row_dict)
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading per score from Hbase"
            )
            return None

    def _read_users(self, users: List[User]) -> Optional[
        Dict[
            User,
            List[Tuple[Post, float]]
        ]
    ]:
        """
        Read per score for list of users
        :return: mapping from user to list of (post, score); or None
        """
        try:
            user_to_result: Dict[
                User,
                List[Tuple[Post, float]]
            ] = {}
            keys: List[bytes] = [
                self._gen_key(user=user) for user in users
            ]
            with self.connector.get_connection() as connection:
                if connection is None:
                    return None
                table: Table = connection.table(self.table_name)
                for row_key, row_dict in table.rows(
                    rows=keys, columns=self.columns
                ):
                    user: Optional[User] = self._parse_key(key=row_key)
                    if (
                            user is None or
                            row_dict is None
                    ):
                        continue
                    posts_scores: Optional[
                        List[Tuple[Post, float]]
                    ] = self._row_dict_to_posts_scores(row_dict=row_dict)
                    if posts_scores:
                        user_to_result[user] = posts_scores
            return user_to_result
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading per scores from Hbase"
            )
            return None

    def read_users(self, users: List[User]) -> Optional[
        Dict[
            User,
            List[Tuple[Post, float]]
        ]
    ]:
        """
        Read per score for list of users
        :return: mapping from user to list of (post, score); or None
        """
        user_to_result: Dict[
            User,
            List[Tuple[Post, float]]
        ] = {}
        if self.verbose:
            progress_bar = tqdm(
                iterable=range(0, len(users), self.batch_size),
                desc="Reading per results..."
            )
            for start_idx in progress_bar:
                end_idx: int = min(start_idx + self.batch_size, len(users))
                data: Optional[
                    Dict[
                        User,
                        List[Tuple[Post, float]]
                    ]
                ] = self._read_users(users=users[start_idx:end_idx])
                if data:
                    user_to_result.update(data)
            progress_bar.close()
            return user_to_result
        else:
            for start_idx in range(0, len(users), self.batch_size):
                end_idx: int = min(start_idx + self.batch_size, len(users))
                data: Optional[
                    Dict[
                        User,
                        List[Tuple[Post, float]]
                    ]
                ] = self._read_users(users=users[start_idx:end_idx])
                if data:
                    user_to_result.update(data)
            return user_to_result


class BaseHbasePerScoreReaderVersion1Config(BasePerScoreReaderConfig, ABC):
    """
    Config for read per recommend result from Hbase
    """
    def __init__(
            self, connector_config: BaseHbaseConnectorProxyConfig,
            table_name: str, columns: List[bytes],
            batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connection to database
        :param table_name: table that store result
        :param batch_size: batch size of training
        :param verbose: display progress bar
        """
        super(BaseHbasePerScoreReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.table_name = table_name
        self.columns = columns
        self.batch_size = batch_size
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
    def columns(self) -> List[bytes]:
        return self._columns

    @columns.setter
    def columns(self, columns: List[bytes]):
        assert isinstance(columns, list)
        assert all(map(lambda x: isinstance(x, bytes), columns))
        self._columns: List[bytes] = columns

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        assert isinstance(batch_size, int)
        self._batch_size: int = batch_size

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose
