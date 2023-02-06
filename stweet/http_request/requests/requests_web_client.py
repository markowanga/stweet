"""Request search_runner class."""
from __future__ import annotations

from typing import Dict, List, Optional

import requests
import requests.adapters
import urllib3
import urllib3.util.ssl_

from ..request_details import RequestDetails
from ..request_response import RequestResponse
from ..web_client import WebClient
from .requests_web_client_proxy_config import RequestsWebClientProxyConfig

_CIPHERS = 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES128-' \
           'GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:' \
           'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-SHA' \
           ':ECDHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA:AES256-SHA'


class _TwitterTLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # FIXME: When urllib3 2.0.0 is out and can be required,
        #  this should use urllib3.util.create_urllib3_context instead of the private, undocumented ssl_ module.
        kwargs['ssl_context'] = urllib3.util.ssl_.create_urllib3_context(ciphers=_CIPHERS)
        return super().init_poolmanager(*args, **kwargs)


class RequestsWebClient(WebClient):
    """Request search_runner class. Implementation based on requests library."""

    proxy: Optional[RequestsWebClientProxyConfig]
    verify: bool

    def __init__(
            self,
            proxy: Optional[RequestsWebClientProxyConfig] = None,
            verify: bool = True,
            interceptors: Optional[List[WebClient.WebClientInterceptor]] = None
    ):
        """Constructor of RequestsWebClient."""
        interceptors_to_super = interceptors \
            if interceptors is not None \
            else []
        super(RequestsWebClient, self).__init__(interceptors_to_super)
        self.proxy = proxy
        self.verify = verify

    def run_clear_request(self, params: RequestDetails) -> RequestResponse:
        """Main method to run request using requests package."""
        session = requests.Session()
        adapter = _TwitterTLSAdapter()
        session.mount('https://twitter.com', adapter)
        session.mount('https://api.twitter.com', adapter)
        response = session.request(
            method=params.http_method.name,
            url=params.url,
            params=params.params,
            headers=params.headers,
            timeout=params.timeout,
            proxies=self._get_proxy(),
            verify=self.verify
        )
        return RequestResponse(response.status_code, response.text)

    def _get_proxy(self) -> Dict[str, str]:
        return None if self.proxy is None else dict({
            'http': self.proxy.http_proxy,
            'https': self.proxy.https_proxy,
        })
