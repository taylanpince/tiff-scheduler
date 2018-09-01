#!/usr/bin/env python

import requests
import sys

from datetime import datetime
from urlparse import urlparse
from dateutil import parser
from pprint import pprint


FILM_DETAIL_URL = "http://www.tiff.net/data/films/%(slug)s.json"

FILM_URLS = (
    "http://www.tiff.net/tiff/call-me-by-your-name/",
    "http://www.tiff.net/tiff/a-ciambra/",
    # "http://www.tiff.net/tiff/short-cuts-programme-02/",
    "http://www.tiff.net/tiff/the-legend-of-the-ugly-king/",
    "http://www.tiff.net/tiff/faces-places/?v=faces-places",
    "http://www.tiff.net/tiff/in-the-fade/",
    "http://www.tiff.net/tiff/happy-end/",
    "http://www.tiff.net/tiff/the-other-side-of-hope",
    "http://www.tiff.net/tiff/a-fantastic-woman",
    "http://www.tiff.net/tiff/soldiers-story-from-ferentari/",
    "http://www.tiff.net/tiff/sheikh-jackson/",
    "http://www.tiff.net/tiff/lady-bird/",
    "http://www.tiff.net/tiff/mary-shelley/",
)

EKIN_FILM_URLS = (
    "http://www.tiff.net/tiff/catch-the-wind/",
    "http://www.tiff.net/tiff/jane/",
    "http://www.tiff.net/tiff/boom-for-real-the-late-teenage-years-of-jean-michel-basquiat/",
    "http://www.tiff.net/tiff/one-of-us/",
    "http://www.tiff.net/tiff/redoubtable/",
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
    sys.exit(main(EKIN_FILM_URLS, optimize_for="day"))
