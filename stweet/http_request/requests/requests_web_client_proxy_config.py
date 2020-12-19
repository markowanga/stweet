"""Configuration of proxy to RequestsWebClient."""
from dataclasses import dataclass


@dataclass
class RequestsWebClientProxyConfig:
    """Configuration class of proxy to RequestsWebClient."""

    http_proxy: str
    https_proxy: str
