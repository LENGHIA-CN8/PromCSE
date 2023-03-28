from typing import Optional, List, Tuple
from logger import SingletonLogger
from objects import Post
from .base_all_posts_reader import (
    BaseAllPostsReader, BaseAllPostsReaderConfig
)
from connector_proxies import (
    BaseMySQLConnectorProxy, BaseMySQLConnectorProxyConfig
)
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from abc import ABC, abstractmethod


class BaseMySQLAllPostsReaderVersion1(BaseAllPostsReader, ABC):
    """
    Read posts from MySQL
    """
    def __init__(
            self, connector: BaseMySQLConnectorProxy
    ):
        """
        Init method
        :param connector: connection to database
        """
        super(BaseMySQLAllPostsReaderVersion1, self).__init__()
        self.connector = connector

    @property
    def connector(self) -> BaseMySQLConnectorProxy:
        return self._connector

    @connector.setter
    def connector(self, connector: BaseMySQLConnectorProxy):
        assert isinstance(connector, BaseMySQLConnectorProxy)
        self._connector: BaseMySQLConnectorProxy = connector

    @abstractmethod
    def _get_sql_command(self) -> str:
        """
        Get sql command for query
        :return: sql command
        """
        pass

    @abstractmethod
    def _get_post_from_tuple_data(
            self, data: Tuple
    ) -> Optional[Post]:
        """
        Get post from a tuple
        :param data: tuple data
        :return: post object if success, else None
        """
        pass

    def read_posts(self) -> Optional[List[Post]]:
        """
        Read list of posts
        :return: list of posts, None if failed
        """
        try:
            sql_command: str = self._get_sql_command()
            connection: Optional[MySQLConnection] = self.connector.get_connection()
            if connection is None:
                return None
            cursor: MySQLCursor = connection.cursor()
            cursor.execute(sql_command)
            posts: List[Post] = []
            for data in cursor.fetchall():
                post: Optional[Post] = self._get_post_from_tuple_data(data=data)
                if post is not None:
                    posts.append(post)
            cursor.close()
            connection.close()
            return posts
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading all posts from MySQL"
            )
            return None


class BaseMySQLAllPostsReaderVersion1Config(BaseAllPostsReaderConfig, ABC):
    """
    Config for read posts from MySQL
    """
    def __init__(
            self, connector_config: BaseMySQLConnectorProxyConfig
    ):
        """
        Init method
        :param connector_config: connection to database
        """
        super(BaseMySQLAllPostsReaderVersion1Config, self).__init__()
        self.connector_config = connector_config

    @property
    def connector_config(self) -> BaseMySQLConnectorProxyConfig:
        return self._connector_config

    @connector_config.setter
    def connector_config(self, connector_config: BaseMySQLConnectorProxyConfig):
        assert isinstance(connector_config, BaseMySQLConnectorProxyConfig)
        self._connector_config: BaseMySQLConnectorProxyConfig = connector_config

