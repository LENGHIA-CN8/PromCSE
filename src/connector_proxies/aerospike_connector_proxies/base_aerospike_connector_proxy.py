from abc import ABC, abstractmethod
from typing import Optional
from threading import Lock
from aerospike import Client


class BaseAerospikeConnectorProxy(ABC):
    """
    Base class for getting Aerospike client
    """
    def __init__(self):
        super(BaseAerospikeConnectorProxy, self).__init__()
        self._client: Optional[Client] = None
        self._create_client()
        self._lock = Lock()  # for thread-safe

    @abstractmethod
    def _create_client(self):
        """
        Create Aerospike client, set value to self._client
        :return: None
        """
        pass

    @abstractmethod
    def _check_client_status(self) -> bool:
        """
        Check status of Aerospike client
        :return: True if healthy, else False
        """
        pass

    def _auto_check_and_get_client(self):
        """
        Check if self._client is currently healthy, if not, reset this value
        :return:
        """
        if self._check_client_status():
            # server is healthy
            return
        self._lock.acquire()    # get the lock for thread-safe
        # re-check the status
        if not self._check_client_status():
            self._create_client()    # reset the value of self._client
        self._lock.release()    # release the lock
        return

    def get_client(self) -> Optional[Client]:
        """
        Get Aerospike client
        :return: Client, or None if there is no healthy client
        """
        self._auto_check_and_get_client()    # recheck the status of self._client
        return self._client


class BaseAerospikeConnectorProxyConfig(ABC):
    """
    Base config class for getting Aerospike client
    """
    pass

