import pytest

from tests.test_util import remove_all_temp_files


@pytest.fixture(autouse=True, scope="session")
def run_around_tests():
    yield
    remove_all_temp_files()
