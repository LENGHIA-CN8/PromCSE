from abc import ABC, abstractmethod
from typing import Dict
from objects import Post


class BaseGeneralScoreWriter(ABC):
    """
    Base class for writing general score
    """
    @abstractmethod
    def write(self, post_to_score: Dict[Post, float]) -> bool:
        """
        Write general score
        :param post_to_score: mapping from post to score
        :return: True if success, else False
        """
        pass


class BaseGeneralScoreWriterConfig(ABC):
    """
    Base config class for writing general score
    """
    pass
