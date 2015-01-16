#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pyflapjack.jsonapi import Contact, Media
from pyflapjack.jsonapi.base import RelationMixin
from pyflapjack.jsonapi.errors import ResourceAttributeError, \
    ResourceRelationError


def test_id_type():
    with pytest.raises(ResourceAttributeError):
        Contact(id=1, first_name='1', last_name='1', email='1', timezone='1')
    Contact(id='1', first_name='1', last_name='1', email='1', timezone='1')


def test_links():
    links = {
        'entities': ['1', '2']
    }
    c = Contact(
        id='1', links=links, first_name='1', last_name='1', email='1',
        timezone='1')
    assert getattr(c, 'entities') == links['entities']
    assert c.to_dict()['links'] == links


def test_relation_mixin():
    r = RelationMixin('contacts')
    assert not r.path_create  # no path and contact id
    r.contact_id = '100'
    assert not r.path_create  # no path
    setattr(r, 'path', 'media')
    assert r.path_create == 'contacts/100/media'


def test_contact_related_resource(api):
    cid = '100'
    media = Media('sms', 'b@gmail.com', 10, 10, contact_id=cid)
    assert media.path == 'media'
    assert media.path_create == 'contacts/%s/media' % cid
    assert not hasattr(media, 'contact_id')
    # no contact_id
    media = Media('sms', 'b@gmail.com', 10, 10)
    assert not media.path_create
    with pytest.raises(ResourceRelationError) as e:
        api.create(media)
    print e.value.message
    # assign contact_id
    media.contact_id = cid
    assert media.path_create == 'contacts/%s/media' % cid
