from typing import Set
from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)
from string import punctuation


class RemovePunctuationTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Class for removing punctuation from text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(RemovePunctuationTextProcessorVersion1, self).__init__(
            verbose=verbose
        )
        self._punctuation_chars: Set[str] = set(punctuation)

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        return "".join([
            char for char in text
            if char not in self._punctuation_chars
        ])


class RemovePunctuationTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config class for removing punctuation from text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(RemovePunctuationTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
