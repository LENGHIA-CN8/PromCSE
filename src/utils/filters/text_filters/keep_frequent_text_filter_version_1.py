from typing import List, Dict
from .base_text_filter import (
    BaseTextFilterConfig, BaseTextFilter
)


class KeepFrequentTextFilterVersion1(BaseTextFilter):
    """
    Keep texts appear more than a threshold
    """
    def __init__(
            self, threshold: int
    ):
        """
        Init method
        :param threshold: threshold to keep text
        """
        super(KeepFrequentTextFilterVersion1, self).__init__()
        self.threshold = threshold

    @property
    def threshold(self) -> int:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int):
        assert isinstance(threshold, int)
        self._threshold: int = threshold

    def filter(self, texts: List[str]) -> List[str]:
        """
        Filter valid texts
        :param texts: list of texts to check
        :return: valid texts
        """
        text_to_count: Dict[str, int] = {}
        for text in texts:
            text_to_count[text] = text_to_count.get(text, 0) + 1
        return [
            text
            for text, count in text_to_count.items()
            if count >= self.threshold
        ]


class KeepFrequentTextFilterVersion1Config(BaseTextFilterConfig):
    """
    Config for keep texts appear more than a threshold
    """
    def __init__(
            self, threshold: int
    ):
        """
        Init method
        :param threshold: threshold to keep text
        """
        super(KeepFrequentTextFilterVersion1Config, self).__init__()
        self.threshold = threshold

    @property
    def threshold(self) -> int:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int):
        assert isinstance(threshold, int)
        self._threshold: int = threshold
