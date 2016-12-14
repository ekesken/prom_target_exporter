#!/bin/bash

sed -i "s/processes=1/processes=$PROCESSES/g" /prom_target_exporter/uwsgi.ini
supervisord && uwsgi --ini /prom_target_exporter/uwsgi.ini
