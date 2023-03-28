from abc import ABC, abstractmethod
from typing import List, Optional


class BaseTrendingContextReader(ABC):
    """
    Base class for reading trending context
    """
    @abstractmethod
    def read_trending_context(self) -> Optional[List[str]]:
        """
        Reading trending context
        :return: list documents describe trending context, or None if failed
        """
        pass


class BaseTrendingContextReaderConfig(ABC):
    """
    Base config class for reading trending context
    """
    pass

