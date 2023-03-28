from typing import Optional
from .base_object_reader import (
    BaseObjectReader, BaseObjectReaderConfig
)
import pickle
from logger import SingletonLogger


class PickleObjectReaderVersion1(BaseObjectReader):
    """
    Read object by Pickle
    """
    def __init__(self, file_name: str):
        """
        Init method
        :param file_name: file to read object from
        """
        super(PickleObjectReaderVersion1, self).__init__()
        self.file_name = file_name

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        assert isinstance(file_name, str)
        self._file_name: str = file_name

    def read_object(self) -> Optional[object]:
        """
        Read object
        :return: object if success, else None
        """
        try:
            with open(self.file_name, mode="rb") as file_obj:
                data: object = pickle.load(file_obj)
            return data
        except:
            SingletonLogger.get_instance().exception(
                "Exception while reading object from file by pickle"
            )
            return None


class PickleObjectReaderVersion1Config(BaseObjectReaderConfig):
    """
    Config for read object by Pickle
    """
    def __init__(self, file_name: str):
        """
        Init method
        :param file_name: file to read object from
        """
        super(PickleObjectReaderVersion1Config, self).__init__()
        self.file_name = file_name

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        assert isinstance(file_name, str)
        self._file_name: str = file_name
