import stweet as st

_RESOURCES_PATH = 'tests/resources'


def test_tweets_csv_import_v1_1_2():
    csv_filename = f'{_RESOURCES_PATH}/tweets_v1.1.2.csv'
    tweets_from_csv = st.read_tweets_from_csv_file(csv_filename)
    assert len(tweets_from_csv) == 9


def test_tweets_json_import_v1_1_2():
    jl_filename = f'{_RESOURCES_PATH}/tweets_v1.1.2.jl'
    tweets_from_csv = st.read_tweets_from_json_lines_file(jl_filename)
    assert len(tweets_from_csv) == 9


def test_user_csv_import_v1_3_0():
    csv_filename = f'{_RESOURCES_PATH}/users_v1.3.0.csv'
    users = st.read_users_from_csv_file(csv_filename)
    assert len(users) == 2


def test_user_json_import_v1_3_0():
    jl_filename = f'{_RESOURCES_PATH}/users_v1.3.0.jl'
    users = st.read_users_from_json_lines_file(jl_filename)
    assert len(users) == 2
