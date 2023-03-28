from typing import List
from .base_text_filter import (
    BaseTextFilter, BaseTextFilterConfig
)


class RemoveDuplicateTextFilterVersion1(BaseTextFilter):
    """
    Remove duplicate text
    """
    def filter(self, texts: List[str]) -> List[str]:
        """
        Filter valid texts
        :param texts: list of texts to check
        :return: valid texts
        """
        return list(set(texts))


class RemoveDuplicateTextFilterVersion1Config(BaseTextFilterConfig):
    """
    Config for remove duplicate text
    """
    pass
