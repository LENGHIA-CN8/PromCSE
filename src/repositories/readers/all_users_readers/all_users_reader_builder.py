from .base_all_users_reader import (
    BaseAllUsersReader, BaseAllUsersReaderConfig
)
from .hbase_all_users_reader_version_1 import (
    HbaseAllUsersReaderVersion1, HbaseAllUsersReaderVersion1Config
)
from .aerospike_all_users_reader_version_1 import (
    AerospikeAllUsersReaderVersion1, AerospikeAllUsersReaderVersion1Config
)
from .with_info_all_users_reader_version_1 import (
    WithInfoAllUsersReaderVersion1,
    WithInfoAllUsersReaderVersion1Config
)
from repositories.readers.user_readers import (
    UserReaderBuilder
)
from connector_proxies import (
    HbaseConnectorProxyFlyweight,
    AerospikeConnectorProxyFlyweight
)
from .api_all_users_reader_version_1 import (
    ApiAllUsersReaderVersion1, ApiAllUsersReaderVersion1Config
)


class AllUsersReaderBuilder:
    """
    Class for building all users reader
    """
    @classmethod
    def build_all_users_reader(
            cls, config: BaseAllUsersReaderConfig
    ) -> BaseAllUsersReader:
        if isinstance(
            config, HbaseAllUsersReaderVersion1Config
        ):
            return HbaseAllUsersReaderVersion1(
                connector=HbaseConnectorProxyFlyweight.get_hbase_connector_proxy(
                    config=config.connector_config
                ),
                table_name=config.table_name,
                column=config.column
            )
        elif isinstance(
            config, WithInfoAllUsersReaderVersion1Config
        ):
            return WithInfoAllUsersReaderVersion1(
                all_users_reader=cls.build_all_users_reader(
                    config=config.all_users_reader_config
                ),
                user_reader=UserReaderBuilder.build_user_reader(
                    config=config.user_reader_config
                )
            )
        elif isinstance(
            config, ApiAllUsersReaderVersion1Config
        ):
            return ApiAllUsersReaderVersion1(
                url=config.url, domain=config.domain, num_days=config.num_days
            )
        elif isinstance(
            config, AerospikeAllUsersReaderVersion1Config
        ):
            return AerospikeAllUsersReaderVersion1(
                connector=AerospikeConnectorProxyFlyweight.get_aerospike_connector_proxy(
                    config=config.connector_config
                ),
                ae_namespace=config.ae_namespace,
                ae_set=config.ae_set
            )
        else:
            raise ValueError(
                f"Invalid class for all users reader: {config}"
            )

