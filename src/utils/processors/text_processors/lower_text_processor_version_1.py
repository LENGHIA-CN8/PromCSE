from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)


class LowerTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Convert text to lower-cased
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(LowerTextProcessorVersion1, self).__init__(
            verbose=verbose
        )

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        return text.lower()


class LowerTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config for convert text to lower-cased
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(LowerTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
