import stweet as st

_RESOURCES_PATH = 'tests/resources'


def test_tweets_csv_import_v1_1_2():
    csv_filename = f'{_RESOURCES_PATH}/tweets_v1.1.2.csv'
    tweets_from_csv = st.read_tweets_from_csv_file(csv_filename)
    assert len(tweets_from_csv) == 9


def test_tweets_json_import_v1_1_2():
    jl_filename = f'{_RESOURCES_PATH}/tweets_v1.1.2.json'
    tweets_from_csv = st.read_tweets_from_json_lines_file(jl_filename)
    assert len(tweets_from_csv) == 9
