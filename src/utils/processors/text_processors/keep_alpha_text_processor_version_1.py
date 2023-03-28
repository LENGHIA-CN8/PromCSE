from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)


class KeepAlphaTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Keep alphabet characters in text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(KeepAlphaTextProcessorVersion1, self).__init__(
            verbose=verbose
        )

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        result: str = ""
        for char in text:
            if char.isalpha():
                result += char
            else:
                result += " "
        return result


class KeepAlphaTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config for keep alphabet characters in text
    """
    def __init__(
            self, verbose: bool
    ):
        """
        Init method
        :param verbose: display progress bar
        """
        super(KeepAlphaTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
