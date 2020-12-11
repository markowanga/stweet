import stweet as st

_username = 'RealDonaldTrump'


def test_get_user():
    task = st.GetUserTask(_username)
    task_result = st.GetUserRunner(task).run()
    assert _username.lower() == task_result.user.screen_name.lower()
