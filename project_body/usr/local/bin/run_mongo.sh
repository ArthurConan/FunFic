#!/bin/bash
mongod --replSet rs0 --enableMajorityReadConcern --storageEngine wiredTiger --dbpath /srv/data/mongo --noprealloc --journal
