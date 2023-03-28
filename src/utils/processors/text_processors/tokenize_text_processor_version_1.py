from pyvi.ViTokenizer import tokenize
from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)
from logger import SingletonLogger


class TokenizeTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Tokenize text with pyvi
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(TokenizeTextProcessorVersion1, self).__init__(
            verbose=verbose
        )

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        try:
            return tokenize(text)
        except:
            SingletonLogger.get_instance().exception(
                "Exception while tokenize text with Pyvi"
            )
            return text


class TokenizeTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config for tokenize text with pyvi
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(TokenizeTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
