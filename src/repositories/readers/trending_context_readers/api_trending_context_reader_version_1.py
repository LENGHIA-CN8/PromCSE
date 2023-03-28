from typing import Optional, List
from logger import SingletonLogger
from .base_trending_context_reader import (
    BaseTrendingContextReader, BaseTrendingContextReaderConfig
)
import requests


class ApiTrendingContextReaderVersion1(BaseTrendingContextReader):
    """
    Reading trending context from Api
    """
    def __init__(
            self, url: str
    ):
        """
        Init method
        :param url: url to get trending context
        """
        super(ApiTrendingContextReaderVersion1, self).__init__()
        self.url = url

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        assert isinstance(url, str)
        self._url: str = url

    def read_trending_context(self) -> Optional[List[str]]:
        """
        Reading trending context
        :return: list documents describe trending context, or None if failed
        """
        try:
            response = requests.get(
                url=self.url
            ).json()
            if (
                not isinstance(response, dict) or
                "context" not in response or
                not isinstance(response["context"], list) or
                not all(map(lambda x: isinstance(x, str),
                            response["context"]))
            ):
                return None
            return response["context"]
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading trending context from Api"
            )
            return None


class ApiTrendingContextReaderVersion1Config(BaseTrendingContextReaderConfig):
    """
    Config for reading trending context from Api
    """
    def __init__(
            self, url: str
    ):
        """
        Init method
        :param url: url to get trending context
        """
        super(ApiTrendingContextReaderVersion1Config, self).__init__()
        self.url = url

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        assert isinstance(url, str)
        self._url: str = url
