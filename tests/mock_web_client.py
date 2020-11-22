from typing import Optional

import stweet as st
from stweet.http_request import RequestDetails, RequestResponse


class MockWebClient(st.WebClient):
    status_code: Optional[int]
    text: Optional[str]

    def __init__(self, status_code: Optional[int], text: Optional[str]):
        self.status_code = status_code
        self.text = text

    def run_request(self, params: RequestDetails) -> RequestResponse:
        return RequestResponse(self.status_code, self.text)

