#!/usr/bin/python
# coding=utf-8
# pylint: disable=I0011,W0702
""" Tool to add new user to database """


import os
import hashlib
import argparse
import binascii

from pymongo import MongoClient
from pymongo import ReadPreference


def main():
    """ Entry point """
    parser = argparse.ArgumentParser(
        description="Tool to add new user to database")
    parser.add_argument("login", help="user login")
    parser.add_argument("password", help="user password")
    parser.add_argument("id", type=int, help="user ID")
    args = parser.parse_args()
    mongo = MongoClient(
        [
            "192.168.5.21",
            "192.168.5.22",
            "192.168.5.23"
        ],
        replicaSet="rs0",
        read_preference=ReadPreference.PRIMARY_PREFERRED,
        readConcernLevel="majority",
        w=2, wtimeout=3000, j=True
    )
    user = mongo["fanficbook"]["users"].find_one({"login": args.login})
    if user is not None:
        print "User {} already exists!".format(args.login)
        return
    salt = os.urandom(64)
    dkey = hashlib.pbkdf2_hmac("sha512", args.password, salt, 100000)
    mongo["fanficbook"]["users"].insert_one({
        "login": args.login,
        "password": binascii.hexlify(dkey),
        "salt": binascii.hexlify(salt),
        "id": args.id
    })
    print "Added {}".format(args.login)


if __name__ == "__main__":
    main()
