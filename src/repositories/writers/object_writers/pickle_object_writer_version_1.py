from .base_object_writer import (
    BaseObjectWriter, BaseObjectWriterConfig
)
import pickle
from utils.file_utils import (
    check_and_make_directory_from_file_name
)
from logger import SingletonLogger


class PickleObjectWriterVersion1(BaseObjectWriter):
    """
    Write object by pickle
    """
    def __init__(self, file_name: str):
        """
        Init method
        :param file_name: file to write data
        """
        super(PickleObjectWriterVersion1, self).__init__()
        self.file_name = file_name
        check_and_make_directory_from_file_name(
            file_name=self.file_name
        )

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        assert isinstance(file_name, str)
        self._file_name: str = file_name

    def write_object(self, data: object) -> bool:
        """
        Write an object
        :param data: object to write
        :return: True if success, else False
        """
        try:
            with open(self.file_name, mode="wb") as file_obj:
                pickle.dump(data, file_obj)
            return True
        except:
            SingletonLogger.get_instance().exception(
                "Exception while writing object to file by pickle"
            )
            return False


class PickleObjectWriterVersion1Config(BaseObjectWriterConfig):
    """
    Config for write object by pickle
    """
    def __init__(self, file_name: str):
        """
        Init method
        :param file_name: file to write data
        """
        super(PickleObjectWriterVersion1Config, self).__init__()
        self.file_name = file_name
        check_and_make_directory_from_file_name(
            file_name=self.file_name
        )

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        assert isinstance(file_name, str)
        self._file_name: str = file_name
