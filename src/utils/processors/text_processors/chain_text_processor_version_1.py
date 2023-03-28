from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)
from .base_text_processor import (
    BaseTextProcessor,
    BaseTextProcessorConfig
)
from typing import List


class ChainTextProcessorVersion1(BaseElementWiseTextProcessor):
    """
    Chain of processors version 1: processors are saved as a list
    """
    def __init__(
            self, processors: List[BaseTextProcessor],
            verbose: bool
    ):
        """
        Init method
        :param processors: list of processor
        :param verbose: display progress bar
        """
        super(ChainTextProcessorVersion1, self).__init__(
            verbose=verbose
        )
        self.processors = processors

    @property
    def processors(self) -> List[BaseTextProcessor]:
        return self._processors

    @processors.setter
    def processors(self, processors: List[BaseTextProcessor]):
        assert isinstance(processors, list)
        assert all(map(lambda x: isinstance(x, BaseTextProcessor), processors))
        self._processors: List[BaseTextProcessor] = processors

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        for processor in self.processors:
            text: str = processor.process_text(
                text=text
            )
        return text


class ChainTextProcessorVersion1Config(BaseElementWiseTextProcessorConfig):
    """
    Config for chain of processors version 1: processors are saved as a list
    """
    def __init__(
            self, processors_config: List[BaseTextProcessorConfig],
            verbose: bool
    ):
        """
        Init method
        :param processors_config: list of processor
        :param verbose: display progress bar
        """
        super(ChainTextProcessorVersion1Config, self).__init__(
            verbose=verbose
        )
        self.processors_config = processors_config

    @property
    def processors_config(self) -> List[BaseTextProcessorConfig]:
        return self._processors_config

    @processors_config.setter
    def processors_config(self, processors_config: List[BaseTextProcessorConfig]):
        assert isinstance(processors_config, list)
        assert all(map(lambda x: isinstance(x, BaseTextProcessorConfig), processors_config))
        self._processors_config: List[BaseTextProcessorConfig] = processors_config
