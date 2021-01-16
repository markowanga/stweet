import stweet as st

_usernames = ['ProtasiewiczJ', 'donaldtuskEPP']


def test_get_user():
    task = st.GetUsersTask(_usernames)
    task_result = st.GetUsersRunner(task, [st.PrintUserOutput()]).run()
    assert len(_usernames) == task_result.users_count
