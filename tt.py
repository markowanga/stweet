from datetime import datetime

import stweet as st
from stweet.twitter_api.twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor


def try_tweet_by_id_scrap():
    id_task = st.TweetsByIdTask('1349479144225173509')
    filename = 'stweet_outputs/output_raw_id.{}.jl'.format(datetime.now().strftime('%Y-%m-%dT%H.%M.%S'))
    output_json = st.JsonLineFileRawOutput(filename)
    output_print = st.PrintRawOutput()
    st.TweetsByIdRunner(
        tweets_by_id_task=id_task,
        raw_data_outputs=[output_print, output_json],
        web_client=st.RequestsWebClient(proxy=proxy, interceptors=[TwitterAuthWebClientInterceptor()])
    ).run()


if __name__ == '__main__':
    try_tweet_by_id_scrap()
