#!/bin/bash

usage() {
    echo "Usage: $0 <host name>"
    exit 1
}

[ "$1" ] || usage

if [ "$1" == "haproxy" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.1
    exit 0
fi

if [ "$1" == "python1" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.11
    exit 0
fi

if [ "$1" == "python2" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.12
    exit 0
fi

if [ "$1" == "python3" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.13
    exit 0
fi

if [ "$1" == "mongo1" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.21
    exit 0
fi

if [ "$1" == "mongo2" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.22
    exit 0
fi

if [ "$1" == "mongo3" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.23
    exit 0
fi

if [ "$1" == "hazelcast1" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.31
    exit 0
fi

if [ "$1" == "hazelcast2" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.32
    exit 0
fi

if [ "$1" == "hazelcast3" ]; then
    bash set_hostname.sh $1
    bash set_ip.sh 192.168.5.33
    exit 0
fi

echo "Unknown host name!"
exit 1
