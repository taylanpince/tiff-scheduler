#!/usr/bin/env python

import optparse
import requests
import sys

from datetime import datetime
from urllib.parse import urlparse
from dateutil import parser
from pprint import pprint


FILM_DETAIL_URL = "http://www.tiff.net/data/films/%(slug)s.json"


def parse_args():
    """
    Parse command line options into variables
    """
    parser = optparse.OptionParser(usage="Usage: %prog [options]")
    
    parser.add_option("--film-urls", 
        type="string", 
        dest="urls",
        help=("Film URLs to pick from, separated by commas")
    )
    
    parser.add_option("--film-urls-file-path", 
        type="string", 
        dest="filepath",
        help=("File that contains film URLs to pick from")
    )
    
    parser.add_option("--optimize-for", 
        type="choice", 
        dest="optimize_for",
        choices=["day", "evening"], 
        default="evening", 
        help=("Option for optimizing for day or evening times")
    )
    
    (options, args) = parser.parse_args()

    return options


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
    options = parse_args()

    if options.urls:
        urls = options.urls.split(",")
    else:
        with open(options.filepath, "r") as data_file:
            urls = data_file.read().splitlines()
    pprint(urls)
    sys.exit(main(urls, optimize_for=options.optimize_for))
