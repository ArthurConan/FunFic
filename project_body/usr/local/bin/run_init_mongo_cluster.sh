#!/bin/bash
mongo --eval 'rs.initiate({_id:"rs0",members:[{_id:0,host: "192.168.5.21"},{_id:1,host:"192.168.5.22"},{_id:2,host:"192.168.5.23"}]})'
