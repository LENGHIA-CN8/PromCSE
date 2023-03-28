from .base_hbase_connector_proxy import (
    BaseHbaseConnectorProxy, BaseHbaseConnectorProxyConfig
)
from .hbase_connector_proxy_version_1 import (
    HbaseConnectorProxyVersion1, HbaseConnectorProxyVersion1Config
)


class HbaseConnectorProxyBuilder:
    """
    Class for building Hbase connector proxy, according to Builder design pattern
    """
    @classmethod
    def build_hbase_connector_proxy(
            cls, config: BaseHbaseConnectorProxyConfig
    ) -> BaseHbaseConnectorProxy:
        """
        Build the connector proxy
        :param config: BaseHbaseConnectorProxyConfig
        :return: BaseHbaseConnectorProxy
        """
        if isinstance(config, HbaseConnectorProxyVersion1Config):
            return HbaseConnectorProxyVersion1(
                servers=config.servers, port=config.port, pool_size=config.pool_size,
                timeout=config.timeout, transport=config.transport, protocol=config.protocol
            )
        else:
            raise ValueError(
                f"Invalid class for Hbase connector proxy: {config}"
            )
