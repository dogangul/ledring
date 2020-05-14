#!/bin/bash


cp ledring_server.service /lib/systemd/system/

systemctl enable ledring_server.service
systemctl start ledring_server.service
