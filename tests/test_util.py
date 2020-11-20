import glob
import os
import uuid

_temp_file_prefix = 'test_temp_file_'


def get_temp_test_file_name(file_extension_without_dot: str) -> str:
    return '{}{}.{}'.format(_temp_file_prefix, _get_uuid_str(), file_extension_without_dot)


def _get_uuid_str() -> str:
    return uuid.uuid4().__str__().replace('-', '')


def remove_all_temp_files():
    files_to_remove = glob.glob("{}*".format(_temp_file_prefix))
    for filePath in files_to_remove:
        os.remove(filePath)
    return


print(get_temp_test_file_name('csv'))
