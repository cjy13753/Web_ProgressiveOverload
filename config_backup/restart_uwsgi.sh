#!/bin/bash

sudo cp /home/ubuntu/progressiveoverload/config_backup/copy_and_use_uwsgi_progressiveoverload.service /etc/systemd/system/;
sudo rm /etc/systemd/system/uwsgi_progressiveoverload.service;
sudo mv /etc/systemd/system/copy_and_use_uwsgi_progressiveoverload.service /etc/systemd/system/uwsgi_progressiveoverload.service;
sudo systemctl daemon-reload;
sudo systemctl restart uwsgi_progressiveoverload.service