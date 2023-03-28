from abc import ABC, abstractmethod
from typing import Optional
from threading import Lock
from mysql.connector import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool


class BaseMySQLConnectorProxy(ABC):
    """
    Base class for getting MySQL connection
    """
    def __init__(self):
        super(BaseMySQLConnectorProxy, self).__init__()
        self._connection_pool: Optional[MySQLConnectionPool] = None
        self._create_connection_pool()
        self._lock = Lock()   # for thread-safe

    @abstractmethod
    def _create_connection_pool(self):
        """
        Create connection pool to MySQL database
        :return: None
        """
        pass

    @abstractmethod
    def _check_server_status(self) -> bool:
        """
        Check status of MySQL server
        :return: True if healthy, else False
        """
        pass

    def _auto_check_and_create_connection_pool(self):
        """
        Check if self._connection_pool is currently healthy, if not, recreate the connection pool
        :return:
        """
        if self._check_server_status():
            # server is healthy
            return
        self._lock.acquire()    # get the lock for thread-safe
        # re-check the status
        if not self._check_server_status():
            self._create_connection_pool()
        self._lock.release()    # release the lock

    def get_connection(self) -> Optional[MySQLConnection]:
        """
        Get MySQL connection
        :return: MySQl connection, or None if there is no healthy server
        """
        self._auto_check_and_create_connection_pool()    # recheck the status of self._connection_pool
        if self._connection_pool is None:
            return None
        else:
            return self._connection_pool.get_connection()


class BaseMySQLConnectorProxyConfig(ABC):
    """
    Base config class for getting MySQL connection
    """
    pass
