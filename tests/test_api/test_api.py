#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pyflapjack.jsonapi import FlapjackAPI, Contact
from pyflapjack.jsonapi.errors import FlapjackAPIError


def get_request_url(mock_request):
    return mock_request.call_args[0][1]


def test_query(api, mock_200, contact):
    returned = api.query(Contact)
    assert mock_200.is_called
    assert 'contacts' in get_request_url(mock_200)
    assert returned[0].id == contact.id

    returned = api.query(Contact, contact.id)
    assert contact.id in get_request_url(mock_200)
    assert returned[0].id == contact.id


def test_create(api, mock_201, contact):
    returned = api.create(contact)
    assert returned[0] == contact.id


def test_delete(api, mock_204):
    api = FlapjackAPI()
    api.delete(Contact, '1')


def test_url_too_long(api):
    with pytest.raises(FlapjackAPIError):
        api.query(Contact, ','.join(str(i) for i in xrange(1025)))


def test_update():
    pass
