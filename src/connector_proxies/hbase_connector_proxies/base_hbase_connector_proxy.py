from abc import ABC, abstractmethod
from typing import Optional
from threading import Lock
from happybase import Connection, ConnectionPool
import contextlib


class BaseHbaseConnectorProxy(ABC):
    """
    Base class for getting Hbase connection
    """
    def __init__(self):
        super(BaseHbaseConnectorProxy, self).__init__()
        self._connection_pool: Optional[ConnectionPool] = None
        self._create_connection_pool()
        self._lock = Lock()  # for thread-safe

    @abstractmethod
    def _create_connection_pool(self):
        """
        Create connection pool to Hbase: set value to self._connection_pool
        :return: None
        """
        pass

    @abstractmethod
    def _check_server_status(self) -> bool:
        """
        Check status of Hbase server
        :return: True if healthy, else False
        """
        pass

    def _auto_check_and_create_connection_pool(self):
        """
        Check if self._connection_pool is currently healthy, if not, re-create connection pool
        :return:
        """
        if self._check_server_status():
            # server is healthy
            return
        self._lock.acquire()    # get the lock for thread-safe
        # re-check the status
        if not self._check_server_status():
            self._create_connection_pool()    # re-create connection pool
        self._lock.release()    # release the lock

    @contextlib.contextmanager
    def get_connection(self) -> Optional[Connection]:
        """
        Get Hbase connector
        :return: Hbase connector, or None if there is no healthy server
        """
        self._auto_check_and_create_connection_pool()    # recheck the status of self._connection_pool
        if self._connection_pool is None:
            yield None
        else:
            with self._connection_pool.connection() as connection:
                yield connection


class BaseHbaseConnectorProxyConfig(ABC):
    """
    Base config class for getting Hbase connection
    """
    pass

