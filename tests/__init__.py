# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~

    Provides application unit tests
"""

from sys import stderr

from flask.json import loads, dumps
from app import create_app, db

initialized = False


def setup_package():
    """database context creation"""
    global initialized
    global app
    global client
    global jsonx
    global endpoint
    global base

    app = create_app(config_mode='Test')
    endpoint = app.config['API_URL_PREFIX']
    base = '%s/' % endpoint if endpoint else ''
    client = app.test_client()
    jsonx = app.test_request_context()
    jsonx.push()
    initialized = True

    print('Test Package Setup\n')


def teardown_package():
    """database context removal"""
    global initialized
    global jsonx

    jsonx.pop()
    initialized = False

    print('Test Package Teardown\n')


def get_globals():
    global app
    global client
    global jsonx

    return app, client, jsonx


class APIHelper:
    json = 'application/json'

    def get_data(self, table, id=None, query=None):
        # returns status_code 200

        if id:
            url = base + table + '/' + id
        else:
            url = base + table

        if query:
            r = client.get(url, content_type=self.json, q=query)
        else:
            r = client.get(url, content_type=self.json)

        return r

    def delete_data(self, table, id):
        # returns status_code 204
        url = '%s/%s/%s' % (endpoint, table, id)
        r = client.delete(url, content_type=self.json)
        return r

    def post_data(self, data, table):
        # returns status_code 201
        url = base + table
        r = client.post(url, data=dumps(data), content_type=self.json)
        return r

    def patch_data(self, data, table, id=None, query=None):
        # returns status_code 200 or 201
        if id:
            url = base + table + '/' + id
        else:
            url = base + table

        if query:
            r = client.patch(
                url, data=dumps(data), content_type=self.json, q=query)
        else:
            r = client.patch(url, data=dumps(data), content_type=self.json)

        return r

    def get_num_results(self, table):
        r = self.get_data(table)
        loaded = loads(r.data)
        return loaded['num_results']

    def get_type(self, table, id=1):
        r = self.get_data(table, id)
        loaded = loads(r.data)
        return loaded['type']['id']