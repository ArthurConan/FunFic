#!/usr/bin/python
# coding=utf-8
# pylint: disable=I0011,C0103,E1101,R0201,R0903,W0702
"""
Fan Fiction Book

Modules
"""


class ModuleBase(object):
    """ Engine module base class """

    def module_is_avalaible(self):
        """ Check if this module should be shown to current user """
        raise NotImplementedError("Not implemented")
