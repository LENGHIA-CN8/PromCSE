from .base_aerospike_connector_proxy import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from .aerospike_connector_proxy_builder import (
    AerospikeConnectorProxyBuilder
)
from typing import Dict
from threading import Lock
from logger import SingletonLogger


class AerospikeConnectorProxyFlyweight:
    """
    Class for saving Aerospike connector, that can be shared between objects (according to Flyweight pattern)
    """
    __string_to_connector_proxy: Dict[str, BaseAerospikeConnectorProxy] = {}    # save created Aerospike connector
    __lock: Lock = Lock()    # for thread-safe

    @classmethod
    def get_aerospike_connector_proxy(
            cls, config: BaseAerospikeConnectorProxyConfig
    ) -> BaseAerospikeConnectorProxy:
        """
        Get a Aerospike connector proxy
        :param config: BaseAerospikeConnectorProxyConfig
        :return: BaseAerospikeConnectorProxy
        """
        string: str = str(config)
        if string not in cls.__string_to_connector_proxy:
            # connector proxy haven't been created
            cls.__lock.acquire()   # get the lock
            # re-check whether connector proxy have been created
            if string not in cls.__string_to_connector_proxy:
                connector_proxy: BaseAerospikeConnectorProxy = AerospikeConnectorProxyBuilder.build_aerospike_connector_proxy(
                    config=config
                )
                cls.__string_to_connector_proxy[string] = connector_proxy
                SingletonLogger.get_instance().info(f"Create Aerospike connector proxy and store in Flyweight")
            cls.__lock.release()    # release the lock
        return cls.__string_to_connector_proxy[string]
