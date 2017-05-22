#!/usr/bin/python
# coding=utf-8
# pylint: disable=I0011,C0103,E1101,R0201,R0903,W0702,C0111
"""
Fan Fiction Book

Tools
"""


import datetime
import cherrypy
import logging
import pickle
import base64

from cherrypy.lib.sessions import Session


def secureheaders():
    """ Secure headers """
    headers = cherrypy.response.headers
    headers["X-Frame-Options"] = "DENY"
    headers["X-XSS-Protection"] = "1; mode=block"
    headers["Content-Security-Policy"] = "default-src='self'"


class IgnoreRequestFilter(logging.Filter):
    """ Ignore requests on URL """

    def __init__(self, request_to_ignore):
        super(IgnoreRequestFilter, self).__init__()
        self.request_to_ignore = request_to_ignore

    def filter(self, record):
        return self.request_to_ignore not in record.getMessage()


class HazelcastSession(Session):
    """ Support for Hazelcast session """

    servers = ["127.0.0.1:5701"]
    check_interval = 0.01
    max_wait_time = 0.25

    def setup(cls, **kwargs):
        """ Setup. Called once """
        for k, v in kwargs.items():
            setattr(cls, k, v)
        import socket
        socket.setdefaulttimeout(1.0)
        import hazelcast
        config = hazelcast.ClientConfig()
        config.group_config.name = "fanficbook"
        config.group_config.password = "fanficbook"
        config.properties["hazelcast.client.heartbeat.interval"] = 1000
        config.properties["hazelcast.client.heartbeat.timeout"] = 15000
        for server in cls.servers:
            config.network_config.addresses.append(server)
        client = hazelcast.HazelcastClient(config)
        cls.cache = client.get_map("cherrypy").blocking()

    setup = classmethod(setup)

    def _exists(self):
        try:
            return self.cache.contains_key(self.id)
        except:
            cherrypy.log("Error in _exists()")
            return False

    def _load(self):
        try:
            _data = self.cache.get(self.id)
            if _data is not None:
                _data = pickle.loads(base64.b64decode(_data))
            return _data
        except:
            cherrypy.log("Error in _load()")
            return None

    def _save(self, expiration_time):
        current_time = datetime.datetime.now()
        ttl = int(abs((expiration_time - current_time).total_seconds()))
        try:
            self.cache.put(
                self.id,
                base64.b64encode(
                    pickle.dumps(
                        (self._data, expiration_time),
                        pickle.HIGHEST_PROTOCOL
                    )
                ),
                ttl
            )
        except:
            cherrypy.log("Error in _save()")

    def _delete(self):
        try:
            return self.cache.remove(self.id)
        except:
            cherrypy.log("Error in _delete()")

    def acquire_lock(self):
        self.locked = True
        try:
            self.cache.lock(self.id)
        except:
            cherrypy.log("Error in acquire_lock()")

    def release_lock(self):
        try:
            self.cache.unlock(self.id)
            self.locked = False
        except:
            cherrypy.log("Error in release_lock()")
            self.locked = False

    def __len__(self):
        try:
            return self.cache.size()
        except:
            cherrypy.log("Error in __len__()")
            return 0
