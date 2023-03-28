from .base_mysql_connector_proxy import (
    BaseMySQLConnectorProxy, BaseMySQLConnectorProxyConfig
)
from .mysql_connector_proxy_builder import (
    MySQLConnectorProxyBuilder
)
from typing import Dict
from threading import Lock
from logger import SingletonLogger


class MySQLConnectorProxyFlyweight:
    """
    Class for saving MySQL connector, that can be shared between objects (according to Flyweight pattern)
    """
    __string_to_connector_proxy: Dict[str, BaseMySQLConnectorProxy] = {}    # save created MySQL connector
    __lock: Lock = Lock()    # for thread-safe

    @classmethod
    def get_mysql_connector_proxy(
            cls, config: BaseMySQLConnectorProxyConfig
    ) -> BaseMySQLConnectorProxy:
        """
        Get a MySQL connector proxy
        :param config: BaseMySQLConnectorProxyConfig
        :return: BaseMySQLConnectorProxy
        """
        string: str = str(config)
        if string not in cls.__string_to_connector_proxy:
            # connector proxy haven't been created
            cls.__lock.acquire()   # get the lock
            # re-check whether connector proxy have been created
            if string not in cls.__string_to_connector_proxy:
                connector_proxy: BaseMySQLConnectorProxy = MySQLConnectorProxyBuilder.build_mysql_connector_proxy(
                    config=config
                )
                cls.__string_to_connector_proxy[string] = connector_proxy
                SingletonLogger.get_instance().info(
                    f"Create MySQL connector proxy and store in Flyweight"
                )
            cls.__lock.release()    # release the lock
        return cls.__string_to_connector_proxy[string]
