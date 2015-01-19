#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urlparse import urljoin
from requests import Session
from .errors import check_status, ResourceRelationError
from pyflapjack.jsonapi.base import RelationMixin


class FlapjackSession(Session):
    def get(self, url, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update({
            'Accept': 'application/vnd.api+json',
        })
        return super(FlapjackSession, self).get(url, headers=headers, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update({
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
        })
        return super(FlapjackSession, self).post(
            url, data=data, json=json, headers=headers, **kwargs)

    def patch(self, url, data=None, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update({
            'Content-Type': 'application/json-patch+json',
            'Accept': 'application/vnd.api+json',
        })
        return super(FlapjackSession, self).patch(
            url, data=data, headers=headers, **kwargs)


class FlapjackAPI(object):
    def __init__(self, server_url='http://127.0.0.1:3081'):
        self._session = FlapjackSession()
        self._root = server_url

    def _resource_url(self, resource_path, *ids):
        url = urljoin(self._root, resource_path)
        if ids:
            url = '%s/%s' % (url, ','.join(ids))
        return url

    def create(self, *objects):
        """
        Create resource objects

        :param objects: the type of all objects should be the same
        :returns: a list of ids of the created objects
        :raises:
            :class:`.errors.AlreadyExistsError` or
            :class:`.errors.InvalidDataError`
        """
        obj = objects[0]
        data = {obj.path: [o.to_dict() for o in objects]}
        if isinstance(obj, RelationMixin):
            path = obj.path_create
            if not path:
                raise ResourceRelationError(
                    '%s id must be set before a %s object can be saved' % (
                    obj.relate_path, obj.path))
        else:
            path = obj.path
        path = self._resource_url(path)
        resp = self._session.post(path, json=data)
        check_status(201, resp, path=path)
        return resp.json()

    def query(self, resource_cls, *ids):
        """
        Get objects from resource

        :param resource_cls:
            a subclass of :class:`.base.Resource`.
        :param ids: if not given, get all objects.
        :return: instances of the given resource class
        :raises:
            :class:`.errors.NotFoundError`
        """
        path = self._resource_url(resource_cls.path, *ids)
        resp = self._session.get(path)
        check_status(200, resp, path=path)
        resp = resp.json()
        objects = resp[resource_cls.path]
        return [resource_cls.from_dict(o) for o in objects]

    def update(self, resource_cls, patches, *ids):
        """
        Patch objects

        :param resource_cls:
            a subclass of :class:`.base.Resource`.
        :param patches:
            a list of :obj:`.base.ResourcePatch`.
        :param ids: specify which objects to patch
        :raises:
            :class:`.errors.NotFoundError`.
        """
        if not (ids and patches):
            return
        path = self._resource_url(resource_cls.path, *ids)
        resp = self._session.patch(path, json=patches)
        check_status(204, resp, path=path, patches=patches)

    def delete(self, resource_cls, *ids):
        """
        Delete objects

        :param resource_cls:
            a subclass of :class:`.base.Resource`.
        :param ids: specify which objects to patch
        :raises:
            :class:`.errors.NotFoundError`.
        """
        if not ids:
            return
        path = self._resource_url(resource_cls.path, *ids)
        resp = self._session.delete(path)
        check_status(204, resp, path=path, ids=ids)

