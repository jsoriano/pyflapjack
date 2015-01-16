#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyflapjack.utils import FlapjackError


class FlapjackAPIError(FlapjackError):
    pass


class UnknownError(FlapjackAPIError):
    pass


class AlreadyExistsError(FlapjackAPIError):
    pass


class NotFoundError(FlapjackAPIError):
    pass


class InConsistentError(FlapjackAPIError):
    pass


class InvalidDataError(FlapjackAPIError):
    pass


class ResourceAttributeError(FlapjackError):
    pass


class ResourceRelationError(FlapjackAPIError):
    pass


_api_error_map = {
    404: NotFoundError,
    405: InvalidDataError,
    409: AlreadyExistsError,
    422: InConsistentError,
}


def check_status(expected, resp, **context):
    if resp.status_code == expected:
        return
    err_cls = None
    try:
        err_cls = _api_error_map[resp.status_code]
    except KeyError:
        err_cls = UnknownError
    raise err_cls('[%d]resp: %s; context: %s' % (
        resp.status_code, resp.content, context))
