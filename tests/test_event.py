#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mock import MagicMock
import pytest
from pyflapjack import InvalidFlapjackEvent, FlapjackEvent, FlapjackReceiver


def test_state():
    with pytest.raises(InvalidFlapjackEvent):
        FlapjackEvent(
            entity='test',
            check='test',
            type_='action',
            state='fail',
        )


def test_type():
    with pytest.raises(InvalidFlapjackEvent):
        FlapjackEvent(
            entity='test',
            check='test',
            type_='hell',
            state='ok',
        )


def test_tags():
    with pytest.raises(InvalidFlapjackEvent):
        FlapjackEvent(
            entity='test',
            check='test',
            type_='action',
            state='ok',
            tags='user, test'
        )
    FlapjackEvent(
        entity='test',
        check='test',
        type_='action',
        state='ok',
        tags=None
    )
    FlapjackEvent(
        entity='test',
        check='test',
        type_='action',
        state='ok',
        tags=[]
    )


def test_dumps_json():
    event = FlapjackEvent(
        entity='test',
        check='test',
        type_='action',
        state='ok',
        tags=['user', 'test']
    )
    print event.dumps_json()
    assert isinstance(event.dumps_json(), str)


def test_receiver():
    redis = MagicMock()
    channel = 'events'
    receiver = FlapjackReceiver(redis, channel)
    events = [FlapjackEvent(
        entity='entity1',
        check='ping',
        type_='service',
        state='ok',
    ), FlapjackEvent(
        entity='entity2',
        check='ping',
        type_='service',
        state='ok',
    )]
    receiver.send_events(*events)
    assert redis.lpush.is_called
    sent_events = str(redis.lpush.call_args[0])
    for entity in ('entity1', 'entity2'):
        assert entity in sent_events

