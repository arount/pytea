#!/usr/env/bin python

'''
Gitea API wrapper for Python.
API doc: https://try.gitea.io/api/swagger
'''

import parse
import requests

from pytea.resources import resources


class PyteaRequestException(Exception):
    pass


class API(object):
    '''
    Gitea API wrapper.
    '''

    _api_baseroute = '/api/v1'

    def __init__(self, baseuri, token=None):
        if baseuri.endswith('/'):
            baseuri = baseuri[0:-1]

        self._baseuri = ''.join([baseuri, self._api_baseroute])
        self._token = token

    # Aliases to `call`, this should be prefered entry-points
    def post(self, path, params=None):
        return self.call(path, method='post', params=params)

    def get(self, path, params=None):
        return self.call(path, method='get', params=params)

    def delete(self, path, params=None):
        return self.call(path, method='delete', params=params)

    def patch(self, path, params=None):
        return self.call(path, method='patch', params=params)

    def put(self, path, params=None):
        return self.call(path, method='put', params=params)


    def call(self, path, method, params=None):
        '''
        Compute, check and execute request to API.
        Returns requests.Response object.
        '''
        # Handle parameters
        if params is None:
            params = {}
        method = method.lower()
        resource = self.get_resource(path).copy()

        # Check if request needs auth token
        if path.split('/')[1] == 'admin' and self._token is None:
            raise PyteaRequestException(
                'Resource \'{}\' require an authentification token.'.format(resource['path'])
            )
        else:
            params['token'] = self._token

        # Check if `resource` expect to be called with `method` HTTP method
        if not self._resource_has_method(resource, method):
            raise PyteaRequestException('Resource \'{}\' did not expect method {}'.format(
                resource['path'],
                method.upper()
            ))

        # Check if all required parameters are given
        required_params = self.clean_resource_params(resource['path'], resource[method]['parameters'])
        for key in required_params:
            if key not in params.keys():
                raise PyteaRequestException('Resource \'{}\' with method {} expect parameter \'{}\''.format(
                    resource['path'],
                    method.upper(),
                    key
                ))

        func = getattr(requests, method)
        final_uri = ''.join([self._baseuri, path])
        return func(final_uri, params=params)


    def clean_resource_params(self, resource_path, params):
        '''
        Remove params in resource hash already given in resource's uri.
        Example:
            /foo/{bar}/{baz} expect `bar` and `baz`, but since they are in uri we don't want
            to check that again.

        Returns cleaned params hash
        '''
        to_rm = []
        for name in params:
            if '{{{}}}'.format(name) in resource_path:
                to_rm.append(name)

        for key in to_rm:
            params.pop(key, None)

        return params


    def get_resource(self, path):
        '''
        Returns resource's hash from URI (path)
        Augment resource's hash with non-formated path for convenience.
        Returns augmented resource hash.
        '''
        key = self._get_resource_path(path)
        if key is None:
            raise PyteaRequestException('Path \'{}\' did not match with any resource'.format(path))

        resource = resources[key].copy()
        resource['path'] = key
        return resource


    def _resource_has_method(self, resource, method):
        '''
        Check if `resource` (path to resource) accept `method` (HTTP method).
        '''
        if method not in resource.keys():
            return False
        return True

    def _get_resource_path(self, path):
        '''
        Get raw resource's path (/foo/{bar}) from formatted one (/foo/bar).
        '''
        # Two or more routes can match with `path`
        # The one with more characters is the good one.
        # I guess?..
        possibilities = []
        for method in resources:
            compiled = parse.compile(method)
            reparsed = compiled.parse(path)
            if reparsed is not None:
                possibilities.append(method)

        if len(possibilities) == 0:
            return None

        # Return only best possibility
        return sorted(possibilities, key=len)[-1]

