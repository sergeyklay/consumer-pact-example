# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Client module for Consumer API example."""

import json

from asdicts.dict import intersect_keys, merge
from requests.exceptions import (
    ConnectionError,
    RequestException,
    RetryError
)
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from urllib3.exceptions import MaxRetryError

from . import __url__, __version__
from . import exceptions, session
from .resources.products import Products


def default_user_agent() -> str:
    """Return a string representing the default user agent."""
    return f'consumer-example/{__version__} ({__url__})'


def default_headers() -> CaseInsensitiveDict:
    """Return a dictionary representing the default request headers."""
    return CaseInsensitiveDict({
        # Default 'User-Agent' header.
        # Usually should be replaced with a more specific value.
        'User-Agent': default_user_agent(),

        # Default Content-Type header:
        'Content-Type': 'application/json; charset=utf-8',

        # Default Accept header.
        #
        # The client may pass a list of media type parameters to the
        # server. The server finds out that a valid parameter is included.
        'Accept': 'application/json'
    })


class Client:
    """API client class."""

    DEFAULT_OPTIONS = {
        # API endpoint base URL to connect to.
        'base_url': 'http://localhost',

        # The number to times to retry if API rate limit is reached or a
        # server error occurs. Rate limit retries delay until the rate limit
        # expires, server errors exponentially backoff starting with a 1-second
        # delay.
        'max_retries': 3,

        # Used API version.
        'version': 'v2',

        # The time stop waiting for a response after a given number of seconds.
        # It is not a time limit on the entire response download; rather, an
        # exception is raised if the server has not issued a response for
        # ``timeout`` seconds (more precisely, if no bytes have been received
        # on the underlying socket for ``timeout`` seconds).
        'timeout': 5.0,
    }

    CLIENT_OPTIONS = set(DEFAULT_OPTIONS.keys())

    QUERY_OPTIONS = {
        'q',     # '/v1/{resource}?q=foobar'
        'cid',   # '/v1/{resource}?cid=12'
        'bid',   # '/v1/{resource}?bid=7'
        'page',  # '/v1/{resource}?page=3'
    }

    REQUEST_OPTIONS = {
        'stream',
        'headers',
        'params',
        'data',
        'files',
        'verify',
        'timeout',
    }

    ALL_OPTIONS = CLIENT_OPTIONS | QUERY_OPTIONS | REQUEST_OPTIONS

    def __init__(self, **options):
        """A :class:`Client` object for interacting with API."""
        self.options = merge(self.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})
        self.session = session.factory(
            max_retries=self.options['max_retries'],
        )

        self._init_statuses()

        # Initialize each resource facade and injecting client object into it
        self.products = Products(self, api_version=self.options['version'])

    def request(self, method: str, path: str, **options) -> Response:
        """Dispatches a request to the airSlate API."""
        options = self._merge_options(options)
        url = options['base_url'].rstrip('/') + '/' + path.lstrip('/')

        # Select and formats options to be passed to the request
        request_options = self._parse_request_options(options)

        try:
            response = getattr(self.session, method)(url, **request_options)
            if response.status_code in self.statuses:
                raise self.statuses[response.status_code](response=response)

            # Any unhandled 5xx is a server error
            if 500 <= response.status_code < 600:
                raise exceptions.InternalServerError(response=response)

            return response
        except (MaxRetryError, RetryError) as retry_exc:
            code = 503
            response = None

            if hasattr(retry_exc, 'response') and retry_exc.response:
                response = retry_exc.response
                code = response.status_code

            raise exceptions.RetryApiError(
                code=code,
                status='Exceeded API Rate Limit',
                response=response,
            )
        except ConnectionError as conn_exc:
            message = ('A connection attempt failed because the ' +
                       'connected party did not properly respond ' +
                       'after a period of time, or established connection ' +
                       'failed because connected host has failed to respond.')
            raise exceptions.InternalServerError(
                message=message,
                response=conn_exc.response,
            )
        except RequestException as req_exc:
            raise exceptions.InternalServerError(response=req_exc.response)

    def _init_statuses(self):
        """Create a mapping of status codes to classes."""
        self.statuses = {}
        for cls in exceptions.__dict__.values():
            if isinstance(cls, type) and issubclass(cls, exceptions.ApiError):
                self.statuses[cls().code] = cls

    def get(self, path, query=None, **options) -> Response:
        """Parses GET request options and dispatches a request."""
        # Select query string options.
        query_options = self._parse_query_options(options)

        # Select all unknown options.
        parameter_options = self._parse_parameter_options(options)

        # Values in the ``query`` takes precedence.
        _query = {} if query is None else query
        query = merge(query_options, parameter_options, _query)

        # Values in the ``options['headers']`` takes precedence.
        headers = merge(
            default_headers(),
            options.pop('headers', {})
        )

        # `Content-Type` HTTP header should be set only for PUT and POST
        del headers['Content-Type']

        return self.request('get', path, params=query, headers=headers,
                            **options)

    def post(self, path, data, **options) -> Response:
        """Parses POST request options and dispatches a request."""
        return self._create('post', path, data, **options)

    def _create(self, method, path, data, **options):
        """Internal helper to send POST/PUT/PATCH requests."""
        # Select all unknown options.
        parameter_options = self._parse_parameter_options(options)

        # Values in the ``data`` takes precedence.
        body = merge(parameter_options, data)

        # Values in the ``options['headers']`` takes precedence.
        headers = merge(
            default_headers(),
            options.pop('headers', {})
        )

        return self.request(method, path, data=body, headers=headers,
                            **options)

    def delete(self, path, **options) -> Response:
        """Dispatches a DELETE request."""
        return self.request('delete', path, **options)

    def _parse_parameter_options(self, options):
        """Select all unknown options.

        This function takes a dictionary of options as input and returns a new
        dictionary containing only the unknown options. Unknown options are
        those that are not part of the client, query, or request options.

        :param options: A dictionary of options.
        :type options: dict
        :return: Returns a dictionary containing only the unknown options.
        :rtype: dict

        Usage:

        >>> client = Client()
        >>> client._parse_parameter_options({})
        {}
        >>> client._parse_parameter_options({'foo': 'bar'})
        {'foo': 'bar'}
        >>> client._parse_parameter_options({'timeout': 1.0})
        {}
        """
        options = self._merge_options(options)
        return intersect_keys(options, self.ALL_OPTIONS, invert=True)

    def _parse_query_options(self, options):
        """Select query string options out of the provided options object.

        This function selects query string options from the provided `options`
        object based on the pre-defined :attr:`QUERY_OPTIONS` dictionary.
         It returns a new dictionary containing only the key-value pairs that
         match the keys in :attr:`QUERY_OPTIONS`.

        :param options: Dictionary of query string options.
        :type options: dict
        :return: Returns a dictionary of query string options filtered by the
            pre-defined :attr:`QUERY_OPTIONS`.
        :rtype: dict

        Usage:

        >>> client = Client()
        >>> client._parse_query_options({})
        {}
        >>> client._parse_query_options({'foo': 'bar'})
        {}
        >>> client._parse_query_options({'bid': 42})
        {'bid': 42}
        """
        options = self._merge_options(options)
        return intersect_keys(options, self.QUERY_OPTIONS)

    def _parse_request_options(self, options):
        """Select request options out of the provided options object.

        This function takes a dictionary options as a parameter and returns a
        dictionary containing selected and formatted request options, which
        will be passed to the `requests library for performing an HTTP request.

        :param options: A dictionary of options to be passed to the 'requests'
            library's request methods.
        :type options: dict
        :return: Returns a dictionary of selected and formatted request options
        :rtype: dict

        Usage:

        >>> client = Client()
        >>> client._parse_request_options({})
        {'timeout': 5.0, 'headers': {}}
        >>> client._parse_request_options({'timeout': 10.0})
        {'timeout': 10.0, 'headers': {}}
        >>> client._parse_request_options({'params': {'foo': True}})
        {'timeout': 5.0, 'params': {'foo': 'true'}, 'headers': {}}
        >>> client._parse_request_options({'data': {'foo': 'bar'}})
        {'timeout': 5.0, 'data': '{"foo": "bar"}', 'headers': {}}
        >>> client._parse_request_options({'headers': {'x-header': 'value'}})
        {'timeout': 5.0, 'headers': {'x-header': 'value'}}
        """
        # Merge options with default options
        options = self._merge_options(options)

        # Select request options keys from the provided options object
        request_options = intersect_keys(options, self.REQUEST_OPTIONS)

        # If 'params' is in request_options, format the params values to be
        # JSON serializable
        if 'params' in request_options:
            params = request_options['params']
            for key in params:
                # json.dumps(None) -> 'null'
                # json.dumps(True) -> 'true'
                if isinstance(params[key], bool) or params[key] is None:
                    params[key] = json.dumps(params[key])

        # If 'data' is in request_options, serialize it to JSON, since
        # requests library doesn't do it automatically
        if 'data' in request_options:
            request_options['data'] = json.dumps(request_options['data'])

        # Update headers with request options and return the updated dictionary
        headers = self.headers.copy()
        headers.update(request_options.get('headers', {}))
        request_options['headers'] = headers

        return request_options

    def _merge_options(self, *objects):
        """Merge option objects with the client's object.

        Merges one or more options objects with client's options and returns a
        new options object.
        """
        return merge(self.options, *objects)
