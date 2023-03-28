from typing import Optional, List
from objects import User
from .base_all_users_reader import (
    BaseAllUsersReader, BaseAllUsersReaderConfig
)
from repositories.readers.user_readers import (
    BaseUserReader, BaseUserReaderConfig
)


class WithInfoAllUsersReaderVersion1(BaseAllUsersReader):
    """
    Reading all users, and read additional info for users
    """
    def __init__(
            self, all_users_reader: BaseAllUsersReader,
            user_reader: BaseUserReader
    ):
        """
        Init method
        :param all_users_reader: read all users
        :param user_reader: read user additional info
        """
        super(WithInfoAllUsersReaderVersion1, self).__init__()
        self.all_users_reader = all_users_reader
        self.user_reader = user_reader

    @property
    def all_users_reader(self) -> BaseAllUsersReader:
        return self._all_users_reader

    @all_users_reader.setter
    def all_users_reader(self, all_users_reader: BaseAllUsersReader):
        assert isinstance(all_users_reader, BaseAllUsersReader)
        self._all_users_reader: BaseAllUsersReader = all_users_reader

    @property
    def user_reader(self) -> BaseUserReader:
        return self._user_reader

    @user_reader.setter
    def user_reader(self, user_reader: BaseUserReader):
        assert isinstance(user_reader, BaseUserReader)
        self._user_reader: BaseUserReader = user_reader

    def read_users(self) -> Optional[List[User]]:
        """
        Read list of users
        :return: list of users, None if failed
        """
        users: Optional[List[User]] = self.all_users_reader.read_users()
        if users is None:
            return None
        self.user_reader.read_users(users=users)
        return users


class WithInfoAllUsersReaderVersion1Config(BaseAllUsersReaderConfig):
    """
    Config for reading all users, and read additional info for users
    """
    def __init__(
            self, all_users_reader_config: BaseAllUsersReaderConfig,
            user_reader_config: BaseUserReaderConfig
    ):
        """
        Init method
        :param all_users_reader_config: read all users
        :param user_reader_config: read user additional info
        """
        super(WithInfoAllUsersReaderVersion1Config, self).__init__()
        self.all_users_reader_config = all_users_reader_config
        self.user_reader_config = user_reader_config

    @property
    def all_users_reader_config(self) -> BaseAllUsersReaderConfig:
        return self._all_users_reader_config

    @all_users_reader_config.setter
    def all_users_reader_config(self, all_users_reader_config: BaseAllUsersReaderConfig):
        assert isinstance(all_users_reader_config, BaseAllUsersReaderConfig)
        self._all_users_reader_config: BaseAllUsersReaderConfig = all_users_reader_config

    @property
    def user_reader_config(self) -> BaseUserReaderConfig:
        return self._user_reader_config

    @user_reader_config.setter
    def user_reader_config(self, user_reader_config: BaseUserReaderConfig):
        assert isinstance(user_reader_config, BaseUserReaderConfig)
        self._user_reader_config: BaseUserReaderConfig = user_reader_config
