import requests

from stweet.http_request.request_details import RequestDetails
from stweet.http_request.request_response import RequestResponse


class RequestRunner:

    @staticmethod
    def run_request(params: RequestDetails) -> RequestResponse:
        session = requests.Session()
        response = session.get(url=params.url, params=params.params, headers=params.headers)
        return RequestResponse(response.status_code, response.text)
