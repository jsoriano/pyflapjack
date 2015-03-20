#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .errors import ResourceAttributeError


class ResourcePatch(dict):
    def __init__(self, op, path, value=None):
        super(ResourcePatch, self).__init__(
            self, op=op, path=path)
        if value is not None:
            self['value'] = value


class Resource(object):
    path = ''
    link_key = 'links'

    create_success_code = 201

    def __init__(self, **kwargs):
        self._links = []
        links = kwargs.pop(self.link_key, {})
        for resource, ids in links.iteritems():
            self.__dict__[resource] = ids
            self._links.append(resource)
        self.validate(kwargs)
        self.__dict__.update(kwargs)

    @staticmethod
    def validate(kwargs):
        oid = kwargs.get('id')
        if oid:
            if not isinstance(oid, basestring):
                raise ResourceAttributeError('id must be a string')
            if ',' in oid:
                raise ResourceAttributeError('id cannot contain token ","')

    def attr_patch(self, attr, value):
        if not hasattr(self, attr):
            raise ResourceAttributeError(
                'Resource %s does not have attribute "%s"' % (
                    self.__class__.__name__, attr))
        return ResourcePatch(
            'replace', '/%s/0/%s' % (self.path, attr), value)

    def add_link_patch(self, link, oid):
        return ResourcePatch(
            'add', '/%s/0/links/%s' % (self.path, link), oid)

    def remove_link_patch(self, link, oid):
        return ResourcePatch(
            'remove', '/%s/0/links/%s/%s' % (self.path, link, oid))

    def to_dict(self):
        d = {}
        links = {}
        for k, v in self.__dict__.iteritems():
            if k.startswith('_'):
                continue
            if k in self._links:
                links[k] = v
            else:
                d[k] = v
        if links:
            d['links'] = links
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


class RelationMixin(object):

    def __init__(self, relate_path, resource_id=None):
        self._relate_path = relate_path
        self._resource_id = resource_id

    def __setattr__(self, key, value):
        if key == 'resource_id':
            self.__dict__['_resource_id'] = value
        else:
            super(RelationMixin, self).__setattr__(key, value)

    @property
    def relate_path(self):
        return self._relate_path

    @property
    def path_create(self):
        if self._resource_id and hasattr(self, 'path'):
            return '%s/%s/%s' % (
                self._relate_path, self._resource_id, self.path)

class MaintenanceMixin(RelationMixin):
    @property
    def path_create(self):
        if self._resource_id and hasattr(self, 'path'):
            return '%s/%s' % (self.path, self._resource_id)
