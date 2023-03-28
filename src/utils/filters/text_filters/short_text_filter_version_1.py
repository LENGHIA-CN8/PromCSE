from .base_element_wise_text_filter_version_1 import (
    BaseElementWiseTextFilterVersion1,
    BaseElementWiseTextFilterVersion1Config
)


class ShortTextFilterVersion1(BaseElementWiseTextFilterVersion1):
    """
    Remove text that have number of characters less than a threshold
    """
    def __init__(self, verbose: bool, threshold: int):
        """
        Init method
        :param verbose: display progress bar
        :param threshold: number of character as threshold
        """
        super(ShortTextFilterVersion1, self).__init__(
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
        if len(text) < self.threshold:
            return False
        else:
            return True


class ShortTextFilterVersion1Config(BaseElementWiseTextFilterVersion1Config):
    """
    Config for remove text that have number of characters less than a threshold
    """
    def __init__(self, verbose: bool, threshold: int):
        """
        Init method
        :param verbose: display progress bar
        :param threshold: number of character as threshold
        """
        super(ShortTextFilterVersion1Config, self).__init__(
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
