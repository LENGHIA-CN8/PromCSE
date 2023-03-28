from typing import List
from .base_text_processor import (
    BaseTextProcessor, BaseTextProcessorConfig
)
from abc import ABC
from tqdm import tqdm


class BaseElementWiseTextProcessor(BaseTextProcessor, ABC):
    """
    Base class for processing texts element wise
    """
    def __init__(self, verbose: bool):
        """
        Init method
        :param verbose: display progress bar or not
        """
        super(BaseElementWiseTextProcessor, self).__init__()
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose

    def process_texts(
            self, texts: List[str]
    ) -> List[str]:
        """
        Process list of text
        :param texts: texts to process
        :return: list of texts
        """
        if self.verbose:
            result: List[str] = []
            progress_bar = tqdm(
                iterable=texts, desc="Processing text..."
            )
            for text in progress_bar:
                result.append(
                    self.process_text(text=text)
                )
            progress_bar.close()
            return result
        else:
            return [
                self.process_text(text=text)
                for text in texts
            ]


class BaseElementWiseTextProcessorConfig(BaseTextProcessorConfig, ABC):
    """
    Base class for processing texts element wise
    """
    def __init__(self, verbose: bool):
        """
        Init method
        :param verbose: display progress bar or not
        """
        super(BaseElementWiseTextProcessorConfig, self).__init__()
        self.verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        assert isinstance(verbose, bool)
        self._verbose: bool = verbose
