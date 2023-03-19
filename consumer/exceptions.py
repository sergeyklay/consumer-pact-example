# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Standard exception hierarchy for Consumer API example."""


class BaseError(Exception):
    """Base class for all errors in Consumer API example."""


class ApiError(BaseError):
    """Base class for errors in API endpoints."""

    def __init__(self, code=None, status=None, message=None, response=None):
        self.code = code
        self.status = status
        self.message = message
        self.response = response
        self.errors = {}

        if response is not None:
            json = response.json()

            if 'errors' in json:
                self.errors = json['errors']

            if 'code' in json and self.code is None:
                self.code = int(json['code'])

            if 'status' in json and self.status is None:
                self.status = json['status']

            if 'message' in json and self.message is None:
                self.message = json['message']

        super().__init__(self.message or self.status)


class BadRequest(ApiError):
    """Error raised for all kinds of bad requests.

    Raise if the client sends something to the server cannot handle.
    """

    def __init__(self, response=None):
        super().__init__(
            code=400,
            status='Bad Request',
            response=response
        )


class NotFoundError(ApiError):
    """Error raised when the server can not find the requested resource."""

    def __init__(self, response=None):
        super().__init__(
            code=404,
            status='Not Found',
            response=response
        )


class MethodNotAllowed(ApiError):
    """Error raised when the server can not find the requested resource."""

    def __init__(self, response=None):
        super().__init__(
            code=405,
            status='Method Not Allowed',
            response=response
        )


class UnprocessableContent(ApiError):
    """Error raised when server returns Precondition Required response."""

    def __init__(self, response=None):
        super().__init__(
            code=422,
            status='Unprocessable Content',
            response=response
        )


class PreconditionRequired(ApiError):
    """Error raised when server returns Precondition Required response."""

    def __init__(self, response=None):
        super().__init__(
            code=428,
            status='Precondition Required',
            response=response
        )


class RetryApiError(ApiError):
    """Base class for retryable errors."""

    def __init__(self, code=None, status=None, response=None):
        super().__init__(
            code=code,
            status=status,
            response=response,
        )


class InternalServerError(ApiError):
    """Internal server error class.

    The server has encountered a situation it doesn't know how to handle.
    """

    def __init__(self, status=None, message=None, response=None):
        code = 500
        if response is not None:
            code = response.status_code

        if status is None:
            status = 'Internal Server Error'

        super().__init__(
            code=code,
            status=status,
            message=message,
            response=response,
        )
