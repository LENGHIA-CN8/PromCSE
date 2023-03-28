from pathlib import Path


def extract_directory_from_file_name(
        file_name: str
) -> Path:
    """
    Get directory path where the file is located in
    :param file_name: path of the file
    :return: path of directory contains the file
    """
    path_obj: Path = Path(file_name)
    return path_obj.parent


def check_and_make_directory_from_file_name(
        file_name: str
):
    """
    Check whether the directory contains the file exists or not, if not: create the directory
    :param file_name: path of the file
    :return:
    """
    directory: Path = extract_directory_from_file_name(
        file_name=file_name
    )
    directory.mkdir(parents=True, exist_ok=True)


def check_and_make_directory(
        directory_path: str
):
    """
    Check whether the directory exists or not, if not: create the directory
    :param directory_path: path of the file
    :return:
    """
    directory: Path = Path(directory_path)
    directory.mkdir(parents=True, exist_ok=True)
