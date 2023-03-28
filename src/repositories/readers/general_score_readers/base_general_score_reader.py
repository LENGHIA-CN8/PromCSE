from abc import ABC, abstractmethod
from typing import Optional, Dict
from objects import Post


class BaseGeneralScoreReader(ABC):
    """
    Base class for reading general score
    """
    @abstractmethod
    def read(self) -> Optional[Dict[Post, float]]:
        """
        Read general score
        :return: mapping from post to score, or None if failed
        """
        pass


class BaseGeneralScoreReaderConfig(ABC):
    """
    Base config class for reading general score
    """
    pass
