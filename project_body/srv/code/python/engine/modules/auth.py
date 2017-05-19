#!/usr/bin/python
# coding=utf-8
# pylint: disable=I0011,C0103,E1101,R0201,R0903,W0702
"""
Fan Fiction Book

Auth module
"""


import uuid
import hashlib
import binascii
import cherrypy
import platform

from engine.modules import ModuleBase


class Auth(ModuleBase):
    """ Manages all auth tasks """

    MODULE_NAME = None

    @staticmethod
    def check_login():
        """ Check if user is logged in """
        if "login" in cherrypy.session:
            cherrypy.request.login = cherrypy.session["login"]
        else:
            if cherrypy.request.query_string:
                path = "%s?%s" % (
                    cherrypy.request.path_info, cherrypy.request.query_string)
            else:
                path = cherrypy.request.path_info
            cherrypy.session["login_redirect"] = path
            raise cherrypy.HTTPRedirect("/auth/login")

    def __init__(self, template_engine, mongo):
        self.template_engine = template_engine
        self.mongo = mongo

    def module_is_avalaible(self):
        """ Check if this module should be shown to current user """
        return False

    @cherrypy.expose
    def index(self):
        """ Index """
        self.check_login()
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def login(self, message=None, login=None, password=None, token=None):
        """ Login page / handler """
        if message is not None:
            cherrypy.session["login_token"] = str(uuid.uuid4())
            return self.template_engine.get_template(
                "login.html"
            ).render(
                generator=platform.node(),
                message=message,
                token=cherrypy.session["login_token"]
            )
        if login is None or password is None or token is None:
            cherrypy.session["login_token"] = str(uuid.uuid4())
            return self.template_engine.get_template(
                "login.html"
            ).render(
                generator=platform.node(),
                token=cherrypy.session["login_token"]
            )
        try:
            user = self.mongo["fanficbook"]["users"].find_one({"login": login})
            if user is not None:
                salt = binascii.unhexlify(user["salt"])
                dkey = hashlib.pbkdf2_hmac("sha512", password, salt, 100000)
                if binascii.hexlify(dkey) != user["password"]:
                    user = None
        except:
            raise cherrypy.HTTPRedirect(
                "/auth/login?message=Internal error. Please try again")
        if token != cherrypy.session.get("login_token", "") or user is None:
            raise cherrypy.HTTPRedirect(
                "/auth/login?message=Invalid login or password!")
        cherrypy.session.pop("login_token", "")
        redirect_target = cherrypy.session.pop("login_redirect", "/")
        cherrypy.session.regenerate()
        cherrypy.session["id"] = user["id"]
        cherrypy.session["login"] = user["login"]
        raise cherrypy.HTTPRedirect(redirect_target)

    @cherrypy.expose
    def logout(self):
        """ Logout (clear session) """
        cherrypy.session.clear()
        cherrypy.session.regenerate()
        raise cherrypy.HTTPRedirect("/")
