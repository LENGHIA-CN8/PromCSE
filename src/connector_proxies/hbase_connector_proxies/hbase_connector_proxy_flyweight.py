from .base_hbase_connector_proxy import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from .hbase_connector_proxy_builder import (
    HbaseConnectorProxyBuilder
)
from typing import Dict
from threading import Lock
from logger import SingletonLogger


class HbaseConnectorProxyFlyweight:
    """
    Class for saving Hbase connector, that can be shared between objects (according to Flyweight pattern)
    """
    __string_to_connector_proxy: Dict[str, BaseHbaseConnectorProxy] = {}    # save created Hbase connector
    __lock: Lock = Lock()    # for thread-safe

    @classmethod
    def get_hbase_connector_proxy(
            cls, config: BaseHbaseConnectorProxyConfig
    ) -> BaseHbaseConnectorProxy:
        """
        Get a Hbase connector proxy
        :param config: BaseHbaseConnectorProxyConfig
        :return: BaseHbaseConnectorProxy
        """
        string: str = str(config)
        if string not in cls.__string_to_connector_proxy:
            # connector proxy haven't been created
            cls.__lock.acquire()   # get the lock
            # re-check whether connector proxy have been created
            if string not in cls.__string_to_connector_proxy:
                connector_proxy: BaseHbaseConnectorProxy = HbaseConnectorProxyBuilder.build_hbase_connector_proxy(
                    config=config
                )
                cls.__string_to_connector_proxy[string] = connector_proxy
                SingletonLogger.get_instance().info(
                    f"Create Hbase connector proxy and store in Flyweight"
                )
            cls.__lock.release()    # release the lock
        return cls.__string_to_connector_proxy[string]
