from .base_element_wise_text_filter_version_1 import (
    BaseElementWiseTextFilterVersion1,
    BaseElementWiseTextFilterVersion1Config
)
from typing import List


class ShortTextFilterVersion2(BaseElementWiseTextFilterVersion1):
    """
    Remove text that have number of words less than a threshold
    If number of words less than a threshold and not have uppercase (not a NER) => remove
    """
    def __init__(self, verbose: bool, threshold: int):
        """
        Init method
        :param verbose: display progress bar
        :param threshold: number of words as threshold
        """
        super(ShortTextFilterVersion2, self).__init__(
            verbose=verbose
        )
        self.threshold = threshold

    @property
    def threshold(self) -> int:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int):
        assert isinstance(threshold, int)
        self._threshold: int = threshold

    def _is_valid(self, text: str) -> bool:
        """
        Check if text is valid
        :param text: text to check
        :return: True if valid, else False
        """
        words: List[str] = text.split()
        if len(words) >= self.threshold:
            return True
        for character in text:
            if character.isupper():
                return True
        return False


class ShortTextFilterVersion2Config(BaseElementWiseTextFilterVersion1Config):
    """
    Config for remove text that have number of words less than a threshold
    If number of words less than a threshold and not have uppercase (not a NER) => remove
    """
    def __init__(self, verbose: bool, threshold: int):
        """
        Init method
        :param verbose: display progress bar
        :param threshold: number of words as threshold
        """
        super(ShortTextFilterVersion2Config, self).__init__(
            verbose=verbose
        )
        self.threshold = threshold

    @property
    def threshold(self) -> int:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int):
        assert isinstance(threshold, int)
        self._threshold: int = threshold
