#!/usr/bin/python
# coding=utf-8
# pylint: disable=I0011,C0103,E1101,R0201,R0903,W0702
"""
Fan Fiction Book

Stories module
"""


import uuid
import cherrypy
import platform

from engine.modules import ModuleBase


class Stories(ModuleBase):
    """ Simple stories """

    MODULE_NAME = "Stories"

    def __init__(self, template_engine, mongo):
        self.template_engine = template_engine
        self.mongo = mongo

    def module_is_avalaible(self):
        """ Check if this module should be shown to current user """
        return True

    @cherrypy.expose
    @cherrypy.tools.check_login()
    def index(self, message=None):
        """ Index - show stories """
        cherrypy.session["stories_token"] = str(uuid.uuid4())
        viewpoint = "fanficbook_{}".format(cherrypy.session["id"])
        try:
            return self.template_engine.get_template(
                "stories.html"
            ).render(
                user=cherrypy.session.get("login", None),
                generator=platform.node(),
                back="/",
                message=message,
                token=cherrypy.session["stories_token"],
                stories=reversed(
                    [i for i in self.mongo[viewpoint]["stories"].find()]
                )
            )
        except:
            raise cherrypy.HTTPRedirect("/stories/")

    @cherrypy.expose
    @cherrypy.tools.check_login()
    def add(self, text=None, token=None):
        """ Add note """
        if text is None or token is None:
            raise cherrypy.HTTPRedirect("/stories/?message=Something is bad")
        session_token = cherrypy.session.pop("stories_token", "")
        if token != session_token:
            raise cherrypy.HTTPRedirect("/stories/?message=Something is bad")
        viewpoint = "fanficbook_{}".format(cherrypy.session["id"])
        try:
            self.mongo[viewpoint]["stories"].insert_one({
                "text": text
            })
        except:
            raise cherrypy.HTTPRedirect(
                "/stories/?message=Internal error. Please try again")
        raise cherrypy.HTTPRedirect("/stories/")
