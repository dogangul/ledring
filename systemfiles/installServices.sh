#!/bin/bash


cp ledring_server.service /lib/systemd/system/

systemctl enable ledring_server.service
systemctl start ledring_server.service

cp serverexpose.service /lib/systemd/system/

systemctl enable serverexpose.service
systemctl start serverexpose.service
