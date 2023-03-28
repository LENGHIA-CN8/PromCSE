from typing import List
from .base_text_filter import (
    BaseTextFilter, BaseTextFilterConfig
)
from tqdm import tqdm
from abc import ABC, abstractmethod


class BaseElementWiseTextFilterVersion1(BaseTextFilter, ABC):
    """
    Base class for filter invalid texts by check each text is valid
    """
    def __init__(self, verbose: bool):
        """
        Init method
        :param verbose: display progress bar
        """
        super(BaseElementWiseTextFilterVersion1, self).__init__()
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

    @abstractmethod
    def _is_valid(self, text: str) -> bool:
        """
        Check if text is valid
        :param text: text to check
        :return: True if valid, else False
        """
        pass

    def filter(self, texts: List[str]) -> List[str]:
        """
        Filter valid texts
        :param texts: list of texts to check
        :return: valid texts
        """
        if self.verbose:
            progress_bar = tqdm(
                iterable=texts, desc="Remove invalid text..."
            )
            valid_texts: List[str] = []
            for text in progress_bar:
                if self._is_valid(text=text):
                    valid_texts.append(text)
            progress_bar.close()
            return valid_texts
        else:
            return [
                text for text in texts
                if self._is_valid(text=text)
            ]


class BaseElementWiseTextFilterVersion1Config(BaseTextFilterConfig, ABC):
    """
    Base config class for filter invalid texts by check each text is valid
    """
    def __init__(self, verbose: bool):
        """
        Init method
        :param verbose: display progress bar
        """
        super(BaseElementWiseTextFilterVersion1Config, self).__init__()
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose
