from torch import Tensor
import numpy as np
from scipy.sparse import spmatrix
from typing import Union


EncodeValue = Union[Tensor, spmatrix, np.ndarray]


class Encode:
    """
    Class represent an encode object
    """
    def __init__(self, encode_name: str, timestamp: int, value: EncodeValue):
        """
        Init method
        :param encode_name: name of encode
        :param timestamp: timestamp of encode
        :param value: value of encode
        """
        self.encode_name = encode_name
        self.timestamp = timestamp
        self.value = value

    @property
    def encode_name(self) -> str:
        return self._encode_name

    @encode_name.setter
    def encode_name(self, encode_name: str):
        assert isinstance(encode_name, str)
        self._encode_name: str = encode_name

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int):
        assert isinstance(timestamp, int)
        self._timestamp: int = timestamp

    @property
    def value(self) -> EncodeValue:
        return self._value

    @value.setter
    def value(self, value: EncodeValue):
        assert (
            isinstance(value, np.ndarray) or
            isinstance(value, spmatrix) or
            isinstance(value, Tensor)
        )
        self._value: EncodeValue = value
