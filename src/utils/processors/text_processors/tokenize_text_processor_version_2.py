from .base_element_wise_text_processor import (
    BaseElementWiseTextProcessor,
    BaseElementWiseTextProcessorConfig
)
from vncorenlp import VnCoreNLP
from logger import SingletonLogger


class TokenizeTextProcessorVersion2(BaseElementWiseTextProcessor):
    """
    Tokenize text with vn core nlp
    """
    def __init__(
            self, vn_core_address: str, vn_core_port: int,
            verbose: bool
    ):
        """
        Init method
        :param vn_core_address: address of vn core NLP
        :param vn_core_port: port of vn core NLP
        :param verbose: display progress bar
        """
        super(TokenizeTextProcessorVersion2, self).__init__(
            verbose=verbose
        )
        self._tokenizer = VnCoreNLP(
            address=vn_core_address, port=vn_core_port
        )

    def process_text(self, text: str) -> str:
        """
        Process text
        :param text: text to process
        :return: text
        """
        try:
            return " ".join([
                word
                for sentence in self._tokenizer.tokenize(text=text)
                for word in sentence
            ])
        except:
            SingletonLogger.get_instance().exception(
                "Exception while tokenize text"
            )
            return text


class TokenizeTextProcessorVersion2Config(BaseElementWiseTextProcessorConfig):
    """
    Tokenize text with vn core nlp
    """
    def __init__(
            self, vn_core_address: str, vn_core_port: int,
            verbose: bool
    ):
        """
        Init method
        :param vn_core_address: address of vn core NLP
        :param vn_core_port: port of vn core NLP
        :param verbose: display progress bar
        """
        super(TokenizeTextProcessorVersion2Config, self).__init__(
            verbose=verbose
        )
        self.vn_core_address = vn_core_address
        self.vn_core_port = vn_core_port

    @property
    def vn_core_address(self) -> str:
        return self._vn_core_address

    @vn_core_address.setter
    def vn_core_address(self, vn_core_address: str):
        assert isinstance(vn_core_address, str)
        self._vn_core_address: str = vn_core_address

    @property
    def vn_core_port(self) -> int:
        return self._vn_core_port

    @vn_core_port.setter
    def vn_core_port(self, vn_core_port: int):
        assert isinstance(vn_core_port, int)
        self._vn_core_port: int = vn_core_port
