Web client
==========

Stweet has abstract layer of web client called ``WebClient``. This
abstract class has one easy method to call every request –
``run_request``. Library has also simple classes to perform http request
domain, like ``RequestDetails`` or ``RequestResponse``.

RequestsWebClient
-----------------

``RequestsWebClient`` is the main implementation of ``WebClient`` based
on ``requests`` implementation. ``Requests`` is one of the most popular
library to run http requests.

RequestsWebClient has many features like: - basic http client - proxy -
certificate verification

Constructor of RequestsWebClient have properties: -
**``proxy: Optional[RequestsWebClientProxyConfig] = None``** – proxy
config, when None requests run without proxy -
**``verify: bool = True``** – verification SSL cert, when no library
does not check cert

RequestsWebClientProxyConfig
----------------------------

Config of proxy in RequestsWebClient. It is classic dataclass. Has
properties: - **``http_proxy: str``** – address of http proxy -
**``https_proxy: str``** – address of https proxy

