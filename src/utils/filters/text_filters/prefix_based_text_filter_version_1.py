from .base_element_wise_text_filter_version_1 import (
    BaseElementWiseTextFilterVersion1, BaseElementWiseTextFilterVersion1Config
)
from typing import List


class PrefixBasedTextFilterVersion1(BaseElementWiseTextFilterVersion1):
    """
    Keep text that begin with prefix
    """
    def __init__(
            self, prefixes: List[str], verbose: bool
    ):
        """
        Init method
        :param prefixes: text start with these prefix will be kept
        :param verbose: display progress bar
        """
        super(PrefixBasedTextFilterVersion1, self).__init__(
            verbose=verbose
        )
        self.prefixes = prefixes

    @property
    def prefixes(self) -> List[str]:
        return self._prefixes

    @prefixes.setter
    def prefixes(self, prefixes: List[str]):
        assert isinstance(prefixes, list)
        assert all(map(lambda x: isinstance(x, str), prefixes))
        self._prefixes: List[str] = prefixes

    def _is_valid(self, text: str) -> bool:
        """
        Check if text is valid
        :param text: text to check
        :return: True if valid, else False
        """
        for prefix in self.prefixes:
            if text.startswith(prefix):
                return True
        return False


class PrefixBasedTextFilterVersion1Config(BaseElementWiseTextFilterVersion1Config):
    """
    Config for keep text that begin with prefix
    """
    def __init__(
            self, prefixes: List[str], verbose: bool
    ):
        """
        Init method
        :param prefixes: text start with these prefix will be kept
        :param verbose: display progress bar
        """
        super(PrefixBasedTextFilterVersion1Config, self).__init__(
            verbose=verbose
        )
        self.prefixes = prefixes

    @property
    def prefixes(self) -> List[str]:
        return self._prefixes

    @prefixes.setter
    def prefixes(self, prefixes: List[str]):
        assert isinstance(prefixes, list)
        assert all(map(lambda x: isinstance(x, str), prefixes))
        self._prefixes: List[str] = prefixes
