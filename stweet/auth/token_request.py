"""Util to process access token to Twitter api."""

import re
import time

import requests

from stweet.exceptions import RefreshTokenException


class TokenRequest:
    """Class to manage Twitter token api."""

    _session = requests.Session()
    _retries = 5
    _timeout = 10
    url = 'https://twitter.com'

    def _request(self):
        """Method from Twint."""
        for attempt in range(self._retries + 1):
            # The request is newly prepared on each retry because of potential cookie updates.
            req = self._session.prepare_request(requests.Request('GET', self.url))
            print(f'Retrieving {req.url}')
            try:
                print('self._session.send', req)
                r = self._session.send(req, allow_redirects=True, timeout=self._timeout)
            except requests.exceptions.RequestException as exc:
                if attempt < self._retries:
                    retrying = ', retrying'
                    level = 'WARNING'
                else:
                    retrying = ''
                    level = 'ERROR'
                print(level, f'Error retrieving {req.url}: {exc!r}{retrying}')
            else:
                success, msg = (True, None)
                msg = f': {msg}' if msg else ''

                if success:
                    print(f'{req.url} retrieved successfully{msg}')
                    return r
            if attempt < self._retries:
                sleep_time = 2.0 * 2 ** attempt
                print(f'Waiting {sleep_time:.0f} seconds')
                time.sleep(sleep_time)
        else:
            msg = f'{self._retries + 1} requests to {self.url} failed, giving up.'
            print(msg)
            raise RefreshTokenException(msg)

    def refresh(self) -> str:
        """Method to get refreshed token. In case of error raise RefreshTokenException."""
        print('Retrieving guest token')
        res = self._request()
        match = re.search(r'\("gt=(\d+);', res.text)
        if match:
            print('Found guest token in HTML')
            return str(match.group(1))
        else:
            raise RefreshTokenException('Could not find the Guest token in HTML')
