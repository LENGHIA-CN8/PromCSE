from .base_mysql_connector_proxy import (
    BaseMySQLConnectorProxy, BaseMySQLConnectorProxyConfig
)
from .mysql_connector_proxy_version_1 import (
    MySQLConnectorProxyVersion1, MySQLConnectorProxyVersion1Config
)


class MySQLConnectorProxyBuilder:
    """
    Class for building MySQL connector proxy, according to Builder design pattern
    """
    @classmethod
    def build_mysql_connector_proxy(
            cls, config: BaseMySQLConnectorProxyConfig
    ) -> BaseMySQLConnectorProxy:
        """
        Build the connector proxy
        :param config: BaseMySQLConnectorProxyConfig
        :return: BaseMySQLConnectorProxy
        """
        if isinstance(config, MySQLConnectorProxyVersion1Config):
            return MySQLConnectorProxyVersion1(
                host=config.host, user=config.user, password=config.password,
                database=config.database, pool_size=config.pool_size
            )
        else:
            raise ValueError(
                f"Invalid class for MySQL connector proxy: {config}"
            )
