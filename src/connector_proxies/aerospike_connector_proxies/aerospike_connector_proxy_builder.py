from .base_aerospike_connector_proxy import (
    BaseAerospikeConnectorProxy, BaseAerospikeConnectorProxyConfig
)
from .aerospike_connector_proxy_version_1 import (
    AerospikeConnectorProxyVersion1, AerospikeConnectorProxyVersion1Config
)


class AerospikeConnectorProxyBuilder:
    """
    Class for building Aerospike connector proxy, according to Builder design pattern
    """
    @classmethod
    def build_aerospike_connector_proxy(
            cls, config: BaseAerospikeConnectorProxyConfig
    ) -> BaseAerospikeConnectorProxy:
        """
        Build the connector proxy
        :param config: BaseAerospikeConnectorProxyConfig
        :return: BaseAerospikeConnectorProxy
        """
        if isinstance(config, AerospikeConnectorProxyVersion1Config):
            return AerospikeConnectorProxyVersion1(
                hosts=config.hosts, policies=config.policies
            )
        else:
            raise ValueError(f"Invalid class for Aerospike connector proxy: {config}")
