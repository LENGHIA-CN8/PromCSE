from .base_mysql_connector_proxy import (
    BaseMySQLConnectorProxy,
    BaseMySQLConnectorProxyConfig
)
from mysql.connector import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool
from logger import SingletonLogger


class MySQLConnectorProxyVersion1(BaseMySQLConnectorProxy):
    """
    Class for getting MySQL connection
    Check server status by is_connected() method
    """
    def __init__(
            self, host: str, user: str, password: str,
            database: str, pool_size: int
    ):
        """
        Init method
        :param host: ip of host
        :param user: username
        :param password: password
        :param database: database
        :param pool_size: size of pool
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.pool_size = pool_size
        super(MySQLConnectorProxyVersion1, self).__init__()
        
    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str):
        assert isinstance(host, str)
        self._host: str = host

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, user: str):
        assert isinstance(user, str)
        self._user: str = user

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        assert isinstance(password, str)
        self._password: str = password

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, database: str):
        assert isinstance(database, str)
        self._database: str = database

    @property
    def pool_size(self) -> int:
        return self._pool_size

    @pool_size.setter
    def pool_size(self, pool_size: int):
        assert isinstance(pool_size, int)
        self._pool_size: int = pool_size

    def _create_connection_pool(self):
        """
        Set value to self._connection_pool
        :return: None
        """
        try:
            self._connection_pool = MySQLConnectionPool(
                host=self.host, user=self.user, password=self.password,
                database=self.database, pool_size=self.pool_size
            )
        except:
            SingletonLogger.get_instance().exception(
                "Exception while create MySQL connection"
            )
            self._connection_pool = None

    def _check_server_status(self) -> bool:
        """
        Check status of MySQL server
        :return: True if healthy, else False
        """
        if self._connection_pool is None:
            # No current active server
            return False
        try:
            connection: MySQLConnection = self._connection_pool.get_connection()
            status: bool = connection.is_connected()
            connection.close()
            return status
        except:
            SingletonLogger.get_instance().exception(
                "Exception occur when checking MySQL server status"
            )
            return False


class MySQLConnectorProxyVersion1Config(BaseMySQLConnectorProxyConfig):
    """
    Config class for getting MySQL connection
    Check server status by is_connected() method
    """
    def __init__(
            self, host: str, user: str, password: str,
            database: str, pool_size: int
    ):
        """
        Init method
        :param host: ip of host
        :param user: username
        :param password: password
        :param database: database
        :param pool_size: size of pool
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.pool_size = pool_size
        super(MySQLConnectorProxyVersion1Config, self).__init__()

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str):
        assert isinstance(host, str)
        self._host: str = host

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, user: str):
        assert isinstance(user, str)
        self._user: str = user

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        assert isinstance(password, str)
        self._password: str = password

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, database: str):
        assert isinstance(database, str)
        self._database: str = database

    @property
    def pool_size(self) -> int:
        return self._pool_size

    @pool_size.setter
    def pool_size(self, pool_size: int):
        assert isinstance(pool_size, int)
        self._pool_size: int = pool_size

    def __str__(self) -> str:
        return f"""
        MySQLConnectorProxyVersion1Config     
        host: {self.host}
        user: {self.user}
        password: {self.password}
        database: {self.database}
        pool_size: {self.pool_size}
        """
