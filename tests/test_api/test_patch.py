#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pyflapjack.jsonapi.errors import ResourceAttributeError


def test_attr_patch(contact):
    with pytest.raises(ResourceAttributeError):
        contact.attr_patch('phonenumber', '+8684517800')
    new_email = 'blurrcat2@gmail.com'
    patch = contact.attr_patch('email', new_email)
    assert patch == {
        'op': 'replace',
        'path': '/contacts/0/email',
        'value': new_email
    }


def test_link_patch(contact):
    mid = '12345'
    patch = contact.add_link_patch('media', mid)
    assert patch == {
        'op': 'add',
        'path': '/contacts/0/links/media',
        'value': mid
    }
    patch = contact.remove_link_patch('media', mid)
    assert patch == {
        'op': 'remove',
        'path': '/contacts/0/links/media/' + mid,
    }
