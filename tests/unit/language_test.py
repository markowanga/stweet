import stweet as st


def test_unique_language_shortcut():
    assert len(st.Language) == len(set([it.short_value for it in st.Language]))
