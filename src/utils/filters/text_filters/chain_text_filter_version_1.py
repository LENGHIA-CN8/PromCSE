from .base_text_filter import (
    BaseTextFilter, BaseTextFilterConfig
)
from typing import List


class ChainTextFilterVersion1(BaseTextFilter):
    """
    Chain of filters
    """
    def __init__(
            self, filters: List[BaseTextFilter]
    ):
        """
        Init method
        :param filters: list of filters
        """
        super(ChainTextFilterVersion1, self).__init__()
        self.filters = filters

    @property
    def filters(self) -> List[BaseTextFilter]:
        return self._filters

    @filters.setter
    def filters(self, filters: List[BaseTextFilter]):
        assert isinstance(filters, list)
        assert all(map(lambda x: isinstance(x, BaseTextFilter), filters))
        self._filters: List[BaseTextFilter] = filters

    def filter(self, texts: List[str]) -> List[str]:
        """
        Filter valid texts
        :param texts: list of texts to check
        :return: valid texts
        """
        for node in self.filters:
            texts = node.filter(texts=texts)
        return texts


class ChainTextFilterVersion1Config(BaseTextFilterConfig):
    """
    Chain of filters
    """
    def __init__(
            self, filters_config: List[BaseTextFilterConfig]
    ):
        """
        Init method
        :param filters_config: list of filters
        """
        super(ChainTextFilterVersion1Config, self).__init__()
        self.filters_config = filters_config

    @property
    def filters_config(self) -> List[BaseTextFilterConfig]:
        return self._filters_config

    @filters_config.setter
    def filters_config(self, filters_config: List[BaseTextFilterConfig]):
        assert isinstance(filters_config, list)
        assert all(map(lambda x: isinstance(x, BaseTextFilterConfig), filters_config))
        self._filters_config: List[BaseTextFilterConfig] = filters_config

