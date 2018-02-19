#!/bin/sh
cd /home/app/
exec scrapy runspider pidcheck/spiders/pid_spider.py 2>&1