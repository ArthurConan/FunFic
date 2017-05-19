#!/usr/bin/python
# coding=utf-8
# pylint: disable=I0011,C0103,E1101,R0201,R0903
"""
Fan Fiction Book

Heartbeat module
"""


import cherrypy

from engine.modules import ModuleBase


class Heartbeat(ModuleBase):
    """ Simple heartbeat / avalaible module for haproxy """

    MODULE_NAME = None

    def module_is_avalaible(self):
        """ Check if this module should be shown to current user """
        return False

    @cherrypy.expose
    def index(self):
        """ Index """
        return "OK"
