#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json
import time


class InvalidFlapjackEvent(Exception):
    pass


class FlapjackEvent(dict):
    STATES = ('ok', 'warning', 'critical', 'unknown', 'acknowledgement')
    TYPES = ('action', 'service')

    def __init__(
            self, entity, check, type_, state, timestamp=None, summary='',
            details='', tags=None, perfdata=''):
        """
        Flapjack Event

        :param str entity: Name of the relevant entity (e.g. FQDN)
        :param str check:
            The check name ('service description' in Nagios terminology)
        :param str type_: One of 'service' or 'action'
        :param str state:
            One of 'ok', 'warning', 'critical', 'unknown', 'acknowledgement'
        :param int timestamp: UNIX timestamp of the event's creation
        :param str summary:
            The check output in the case of a service event, otherwise a
            message created for an acknowledgement or similar
        :param str details: Long check output for a Nagios service event
        :param list tags: Performance data for a Nagios service event
        :param str perfdata: Array of tags pertaining to the event
        """
        if type_ not in self.TYPES:
            raise InvalidFlapjackEvent('type "%s" must be one of %s' % (
                type_, self.TYPES))
        if state not in self.STATES:
            raise InvalidFlapjackEvent('state "%s" must be one of %s' % (
                state, self.STATES))
        if tags and not isinstance(tags, list):
            raise InvalidFlapjackEvent('tags must be a list')
        super(FlapjackEvent, self).__init__(
            entity=entity, check=check, type=type_, state=state,
            timestamp=int(timestamp or time.time()), summary=summary,
            details=details, tags=tags, perfdata=perfdata)

    def dumps_json(self):
        return json.dumps(self)


class FlapjackReceiver(object):
    def __init__(self, redis, channel='events'):
        """
        Python Flapjack receiver

        :param redis: a configured redis instance
        :param str channel: channel to send events. Default to 'events'
        """
        self._redis = redis
        self._channel = channel

    def send_events(self, *events):
        """
        Send events to channel

        :param events: one or more instances of :class:`FlapjackEvent`
        :return: length of the channel after the send
        """
        return self._redis.lpush(
            self._channel, *[e.dumps_json() for e in events])
