from abc import ABC, abstractmethod
from typing import List


class BaseTextProcessor(ABC):
    """
    Base class for process text
    """
    @abstractmethod
    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        pass

    @abstractmethod
    def process_texts(self, texts: List[str]) -> List[str]:
        """
        Process list of text
        :param texts: texts to process
        :return: list of texts
        """
        pass


class BaseTextProcessorConfig(ABC):
    """
    Base config class for process text
    """
    pass
