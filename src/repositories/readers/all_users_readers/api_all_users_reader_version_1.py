from typing import Optional, List, Dict
from datetime import date, timedelta
import requests
from objects import User
from .base_all_users_reader import (
    BaseAllUsersReader, BaseAllUsersReaderConfig
)
from logger import SingletonLogger


class ApiAllUsersReaderVersion1(BaseAllUsersReader):
    """
    Read all users from Api
    Only get user ids
    """
    def __init__(
            self, url: str, domain: str, num_days: int
    ):
        """
        Init method
        :param url: url to get data
        :param domain: domain to get data
        :param num_days: num days to get data
        """
        super(ApiAllUsersReaderVersion1, self).__init__()
        self.url = url
        self.domain = domain
        self.num_days = num_days

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        assert isinstance(url, str)
        self._url: str = url

    @property
    def domain(self) -> str:
        return self._domain

    @domain.setter
    def domain(self, domain: str):
        assert isinstance(domain, str)
        self._domain: str = domain

    @property
    def num_days(self) -> int:
        return self._num_days

    @num_days.setter
    def num_days(self, num_days: int):
        assert isinstance(num_days, int)
        self._num_days: int = num_days

    def read_users(self) -> Optional[List[User]]:
        """
        Read list of users
        :return: list of users or None
        """
        try:
            finish_date: date = date.today()
            start_date: date = finish_date - timedelta(days=self.num_days)
            params: Dict[str, str] = {
                "domain": self.domain,
                "start_date": start_date.strftime('%Y-%m-%d'),
                "finish_date": finish_date.strftime('%Y-%m-%d')
            }
            response = requests.get(
                url=self.url, params=params
            )
            if not response.status_code == 200:
                return None
            response = response.json()
            if (
                not isinstance(response, dict) or
                "results" not in response or
                not isinstance(response["results"], list)
            ):
                return None
            users: List[User] = []
            for user_id in response["results"]:
                if isinstance(user_id, str) and user_id.isdigit():
                    users.append(User(user_id=int(user_id)))
            return users
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading users from Api"
            )
            return None


class ApiAllUsersReaderVersion1Config(BaseAllUsersReaderConfig):
    """
    Config for read all users from Api
    Only get user ids
    """
    def __init__(
            self, url: str, domain: str, num_days: int
    ):
        """
        Init method
        :param url: url to get data
        :param domain: domain to get data
        :param num_days: num days to get data
        """
        super(ApiAllUsersReaderVersion1Config, self).__init__()
        self.url = url
        self.domain = domain
        self.num_days = num_days

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        assert isinstance(url, str)
        self._url: str = url

    @property
    def domain(self) -> str:
        return self._domain

    @domain.setter
    def domain(self, domain: str):
        assert isinstance(domain, str)
        self._domain: str = domain

    @property
    def num_days(self) -> int:
        return self._num_days

    @num_days.setter
    def num_days(self, num_days: int):
        assert isinstance(num_days, int)
        self._num_days: int = num_days
