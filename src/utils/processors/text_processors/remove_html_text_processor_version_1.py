from logger import SingletonLogger
from bs4 import BeautifulSoup
from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)


class RemoveHtmlTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Remove Html tags from text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(RemoveHtmlTextProcessorVersion1, self).__init__(
            verbose=verbose
        )

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        try:
            soup = BeautifulSoup(text, parser="lxml", features="lxml")
            return soup.get_text(separator=" ")
        except:
            SingletonLogger.get_instance().exception(
                "Exception while removing Html tags from text"
            )
            return text


class RemoveHtmlTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config for remove Html tags from text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(RemoveHtmlTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
