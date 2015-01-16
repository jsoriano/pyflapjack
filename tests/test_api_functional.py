#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pytest
from pyflapjack.jsonapi import FlapjackAPI, Contact, Media
from pyflapjack.jsonapi.errors import NotFoundError, InConsistentError


api = FlapjackAPI(server_url='http://127.0.0.1:13081')
flapjack_available = False
namespace = str(int(time.time()))


def get_id(resource='', oid=''):
    return '_'.join([namespace, resource, oid or str(int(time.time()))])

try:
    api.query(Contact, get_id('contact', '0'))
except NotFoundError:
    flapjack_available = True
except Exception as e:
    pass
require_flapjack = pytest.mark.skipif(
    not flapjack_available, reason='flapjack server not available')


@pytest.fixture
def contact(request):
    contact = Contact(
        id=get_id('contact', 'test'), email='blurrcat@gmail.com',
        first_name='1', last_name='2', timezone='Europe/London')
    api.create(contact)

    def clean():
        try:
            api.delete(Contact, contact.id)
        except NotFoundError:
            pass
    request.addfinalizer(clean)
    return contact


@require_flapjack
def test_create_query_delete():
    contact = Contact(
        id=get_id('contact', 'test'), email='blurrcat@gmail.com',
        first_name='1', last_name='2', timezone='Europe/London')
    ids = api.create(contact)
    assert ids[0] == contact.id
    contacts = api.query(Contact, contact.id)
    assert contacts[0].email == contact.email
    api.delete(Contact, contact.id)


@require_flapjack
def test_contact_related_resource(contact):
    media = Media('sms', '18615729525', 10, 10, contact_id=contact.id)
    resp = api.create(media)
    assert resp[0] == '%s_%s' % (contact.id, 'sms')
    media.contact_id = get_id('contact', '3')  # invalid contact id
    with pytest.raises(InConsistentError) as e:
        api.create(media)
    print e.value.message


@require_flapjack
def test_patch_attr(contact):
    new_email = 'haha@gmail.com'
    patch = contact.attr_patch('email', new_email)
    api.update(Contact, [patch], contact.id)
    new_contact = api.query(Contact, contact.id)
    assert new_contact[0].email == new_email


@require_flapjack
@pytest.mark.xfail(reason='flapjack API bug: patch remove link not working')
def test_path_link(contact):
    media = Media(
        type_='sms', address='123@123.com', interval=10, rollup_threshold=10,
        contact_id=contact.id
    )
    api.create(media)
    new_contact = api.query(Contact, contact.id)[0]
    assert new_contact.media[0] == '%s_%s' % (new_contact.id, 'sms')
    # remove link
    patch = new_contact.remove_link_patch('media', new_contact.media[0])
    api.update(Contact, [patch], new_contact.id)
    new_contact = api.query(Contact, new_contact.id)[0]
    assert len(new_contact.media) == 0
