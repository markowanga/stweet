import pytest

from tests.test_util import remove_all_temp_files


def prepare_removing_new_files():
    @pytest.fixture(autouse=True)
    def run_around_tests():
        yield
        remove_all_temp_files()
