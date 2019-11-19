#!/bin/bash

[ -f /home/www/ecustCourseInfo/src/courseinfo/data/init.sh ] && sh /home/www/ecustCourseInfo/src/courseinfo/data/init.sh

nginx
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
