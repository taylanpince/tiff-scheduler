#!/usr/bin/env python

import requests
import sys

from datetime import datetime
from urllib.parse import urlparse
from dateutil import parser
from pprint import pprint


FILM_DETAIL_URL = "http://www.tiff.net/data/films/%(slug)s.json"

COUPLE_FILM_URLS = (
    "https://www.tiff.net/tiff/roma/",
    "https://www.tiff.net/tiff/everybody-knows/",
    "https://www.tiff.net/tiff/museo/",
    "https://www.tiff.net/tiff/loro/",
    "https://www.tiff.net/tiff/dogman/",
    "https://www.tiff.net/tiff/meeting-gorbachev/",
    "https://www.tiff.net/tiff/the-wild-pear-tree/",
    "https://www.tiff.net/tiff/saf/",
)

SINGLE_FILM_URLS = (
    "https://www.tiff.net/tiff/maria-by-callas/",
)


def main(urls, optimize_for="evening"):
    days = {}
    
    for url in urls:
        parsed_url = urlparse(url)
        slug = parsed_url.path.replace("/tiff", "").strip("/")
        req = requests.get(FILM_DETAIL_URL % {
            "slug": slug,
        }, headers={
            "Content-Type": "application/json"
        })

        response = req.json()
        schedule_items = response.get("scheduleItems", [])
        title = response.get("title")
        found = False

        for schedule in schedule_items:
            if schedule.get("audienceType", "Public") != "Public":
                continue
            
            start_time = parser.parse(schedule.get("startTime"))
            day = datetime.strftime(start_time, "%B-%-d")
            
            if start_time.hour < 17:
                day += "-day"
            else:
                day += "-evening"

            if days.get(day):
                continue

            if optimize_for == "evening" and (start_time.weekday() < 5 and start_time.hour < 17):
                continue
            elif optimize_for == "day" and (start_time.hour > 14 or start_time.weekday() > 4):
                continue

            days[day] = "%s - %s" % (title, datetime.strftime(start_time, "%A, %B %-d at %-I:%M %p"))
            found = True
            
            break
        
        if not found:
            print("Cannot match %s" % title)
        
    pprint(days)


if __name__ == "__main__":
    sys.exit(main(COUPLE_FILM_URLS, optimize_for="evening"))
