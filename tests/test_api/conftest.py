#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from mock import MagicMock
from pyflapjack.jsonapi import Contact, FlapjackAPI


@pytest.fixture
def contact():
    return Contact(
        id='1', first_name='harry', last_name='L', timezone='Europe/London',
        email='blurrcat@gmail.com')


def mock_request(monkeypatch, status_code, json_data):
    resp = MagicMock()
    resp.configure_mock(**{
        'json.return_value': json_data,
        'status_code': status_code
    })
    m = MagicMock()
    m.configure_mock(**{
        'return_value': resp
    })
    monkeypatch.setattr(
        'pyflapjack.jsonapi.session.FlapjackSession.request', m)
    return m


@pytest.fixture
def mock_200(monkeypatch, contact):
    return mock_request(monkeypatch, 200, {
        'contacts': [contact.to_dict()]
    })


@pytest.fixture
def mock_201(monkeypatch, contact):
    return mock_request(monkeypatch, 201, [contact.id])


@pytest.fixture
def mock_204(monkeypatch):
    return mock_request(monkeypatch, 204, '')


@pytest.fixture
def api():
    return FlapjackAPI()
