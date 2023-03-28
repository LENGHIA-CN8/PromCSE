from typing import Tuple, Optional, List, Dict
from objects import Post
from .base_post_reader import (
    BasePostReader, BasePostReaderConfig
)
from connector_proxies import (
    BaseMySQLConnectorProxy, BaseMySQLConnectorProxyConfig
)
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from logger import SingletonLogger
from tqdm import tqdm
from abc import ABC, abstractmethod


class BaseMySQLPostReaderVersion1(BasePostReader, ABC):
    """
    Base class for reading posts info from MySQL database
    Only read posts from a source news
    """
    def __init__(
            self, connector: BaseMySQLConnectorProxy,
            source_news: str, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector: connector to MySQL database
        :param source_news: source news to read post info
        :param batch_size: batch size of reading
        :param verbose: display progress bar while reading list posts
        """
        super(BaseMySQLPostReaderVersion1, self).__init__()
        self.connector = connector
        self.source_news = source_news
        self.batch_size = batch_size
        self.verbose = verbose

    @property
    def connector(self) -> BaseMySQLConnectorProxy:
        return self._connector

    @connector.setter
    def connector(self, connector: BaseMySQLConnectorProxy):
        assert isinstance(connector, BaseMySQLConnectorProxy)
        self._connector: BaseMySQLConnectorProxy = connector

    @property
    def source_news(self) -> str:
        return self._source_news

    @source_news.setter
    def source_news(self, source_news: str):
        assert isinstance(source_news, str)
        self._source_news: str = source_news

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

    @abstractmethod
    def _get_sql_command_for_post(self, post: Post) -> str:
        """
        Get sql command corresponding to a post
        :param post: post to get sql command
        :return: sql command
        """
        pass

    @abstractmethod
    def _get_sql_command_for_posts(self, posts: List[Post]) -> str:
        """
        Get sql command for collection of posts
        :param posts: posts to get sql command
        :return: sql command
        """
        pass

    @abstractmethod
    def _get_post_from_tuple(
            self, data: Tuple
    ) -> Optional[Post]:
        """
        Get post object from data tuple
        :param data: data tuple
        :return: post object (if success) or None
        """
        pass

    def read_post(self, post: Post) -> bool:
        """
        Read info of a post
        :param post: post to read info
        :return: True if success, else False
        """
        try:
            sql_command: str = self._get_sql_command_for_post(post=post)
            connection: Optional[MySQLConnection] = self.connector.get_connection()
            if connection is None:
                # can not get mysql connection
                return False
            cursor: MySQLCursor = connection.cursor()
            cursor.execute(sql_command)
            data: Optional[Tuple] = cursor.fetchone()
            query_post: Optional[Post] = self._get_post_from_tuple(
                data=data
            ) if data is not None else None
            cursor.close()
            connection.close()
            post.update(other=query_post)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading post info from MySQL"
            )
            return False

    def _read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        try:
            sql_command: str = self._get_sql_command_for_posts(posts=posts)
            connection: Optional[MySQLConnection] = self.connector.get_connection()
            if connection is None:
                # can not get connection to MySQL
                return False
            cursor: MySQLCursor = connection.cursor()
            cursor.execute(sql_command)
            post_to_query_post: Dict[Post, Post] = {}
            for data in cursor.fetchall():
                query_post: Optional[Post] = self._get_post_from_tuple(data=data)
                if query_post is not None:
                    post_to_query_post[query_post] = query_post
            cursor.close()
            connection.close()
            for post in posts:
                post.update(other=post_to_query_post.get(post))
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading posts info from MySQL"
            )
            return False

    def read_posts(self, posts: List[Post]) -> bool:
        """
        Read info of a collection of posts
        :param posts: posts to read info
        :return: True if success, else False
        """
        if self.verbose:
            status: bool = True
            progress_bar = tqdm(
                iterable=range(0, len(posts), self.batch_size),
                desc="Reading posts info..."
            )
            for start_idx in progress_bar:
                end_idx: int = min(start_idx + self.batch_size, len(posts))
                status = self._read_posts(
                    posts=posts[start_idx:end_idx]
                ) and status
            progress_bar.close()
            return status
        else:
            status: bool = True
            for start_idx in range(0, len(posts), self.batch_size):
                end_idx: int = min(start_idx+self.batch_size, len(posts))
                status = self._read_posts(
                    posts=posts[start_idx:end_idx]
                ) and status
            return status


class BaseMySQLPostReaderVersion1Config(BasePostReaderConfig, ABC):
    """
    Base config class for reading posts info from MySQL
    Only read posts from a source news
    """
    def __init__(
            self, connector_config: BaseMySQLConnectorProxyConfig,
            source_news: str, batch_size: int, verbose: bool
    ):
        """
        Init method
        :param connector_config: connector to MySQL database
        :param source_news: source news to read post info
        :param batch_size: batch size of reading
        :param verbose: display progress bar when reading list posts
        """
        super(BaseMySQLPostReaderVersion1Config, self).__init__()
        self.connector_config = connector_config
        self.source_news = source_news
        self.batch_size = batch_size
        self.verbose = verbose

    @property
    def connector_config(self) -> BaseMySQLConnectorProxyConfig:
        return self._connector_config

    @connector_config.setter
    def connector_config(self, connector_config: BaseMySQLConnectorProxyConfig):
        assert isinstance(connector_config, BaseMySQLConnectorProxyConfig)
        self._connector_config: BaseMySQLConnectorProxyConfig = connector_config

    @property
    def source_news(self) -> str:
        return self._source_news

    @source_news.setter
    def source_news(self, source_news: str):
        assert isinstance(source_news, str)
        self._source_news: str = source_news

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

