from typing import List
from abc import ABC, abstractmethod


class BaseTextFilter(ABC):
    """
    Base class for filtered invalid text
    """
    @abstractmethod
    def filter(self, texts: List[str]) -> List[str]:
        """
        Filter valid texts
        :param texts: list of texts to check
        :return: valid texts
        """
        pass


class BaseTextFilterConfig(ABC):
    """
    Base config class for filtered invalid text
    """
    pass
