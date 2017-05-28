#!/bin/bash

usage() {
    echo "Usage: $0 <new ip>"
    exit 1
}

[ "$1" ] || usage

sed -i 's/address \(.*\)/address '"$1"'/g' /etc/network/interfaces

exit 0
