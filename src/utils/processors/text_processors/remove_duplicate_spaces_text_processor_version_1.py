import re
from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)


class RemoveDuplicateSpacesTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Remove duplicate spaces from text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(RemoveDuplicateSpacesTextProcessorVersion1, self).__init__(
            verbose=verbose
        )

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        text: str = re.sub(r'\s+', ' ', text)
        return text.strip()


class RemoveDuplicateSpacesTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config for remove duplicate spaces from text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(RemoveDuplicateSpacesTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
