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
            summary='test',
        )


def test_type():
    with pytest.raises(InvalidFlapjackEvent):
        FlapjackEvent(
            entity='test',
            check='test',
            type_='hell',
            state='ok',
            summary='test',
        )


def test_tags():
    with pytest.raises(InvalidFlapjackEvent):
        FlapjackEvent(
            entity='test',
            check='test',
            type_='action',
            state='ok',
            tags='user, test',
            summary='test',
        )
    FlapjackEvent(
        entity='test',
        check='test',
        type_='action',
        state='ok',
        tags=None,
        summary='test',
    )
    FlapjackEvent(
        entity='test',
        check='test',
        type_='action',
        state='ok',
        tags=[],
        summary='test',
    )


def test_dumps_json():
    event = FlapjackEvent(
        entity='test',
        check='test',
        type_='action',
        state='ok',
        tags=['user', 'test'],
        summary='test',
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
        summary='test',
    ), FlapjackEvent(
        entity='entity2',
        check='ping',
        type_='service',
        state='ok',
        summary='test',
    )]
    receiver.send_events(*events)
    assert redis.lpush.is_called
    sent_events = str(redis.lpush.call_args[0])
    for entity in ('entity1', 'entity2'):
        assert entity in sent_events

