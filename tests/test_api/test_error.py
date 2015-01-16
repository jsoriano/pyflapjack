#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mock import Mock
import pytest
from requests import Response
from pyflapjack.jsonapi.errors import check_status, NotFoundError, UnknownError


def mock_resp(status_code, json_data):
    resp = Response()
    resp.json = Mock(return_value=json_data)
    resp.status_code = status_code
    return resp


def test_check_status_user_error():
    check_status(200, mock_resp(200, None))  # no exception
    cid = '1234'
    with pytest.raises(NotFoundError) as e:
        check_status(
            200, mock_resp(404, {'errors': 'not found'}),
            contact='contact', id=cid)
    msg = e.value.message.lower()
    # context and error information in error message
    assert 'contact' in msg
    assert cid in msg


def test_unexpected_error():
    for code in (400, 503):
        with pytest.raises(UnknownError):
            check_status(
                200, mock_resp(code, None), contact='contact')
