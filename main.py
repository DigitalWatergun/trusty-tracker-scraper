import os
import requests
import argparse
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import scraper.usps_scraper as usps_scraper
import scraper.fedex_scraper as fedex_scraper
from controllers.tracking_hist_controller import *

RDS_USER = os.environ["RDS_USER"]
RDS_PASS = os.environ["RDS_PASS"]
RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_PORT = os.environ["RDS_PORT"]
RDS_DB_NAME = os.environ["RDS_DB_NAME"]


def create_session(): 
    db_string = f"postgresql://{RDS_USER}:{RDS_PASS}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DB_NAME}"
    db = create_engine(db_string)
    Session = sessionmaker(db)
    session = Session()

    return session


def scrape_url(url): 
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text, "html.parser")
    
    return html


def filter_html(html, carrier): 
    if carrier == "usps": 
        trackingInfo = usps_scraper.findTrackingInfo(html)
        return trackingInfo


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Web scraper that takes your carrier and tracking number, then fetches the tracking history for that package.")
    parser.add_argument("tracking_number", metavar="tracking_number", type=str, help="The tracking number you want to track.")
    parser.add_argument("carrier", metavar="carrier", type=str, help="The shipping carrier that uses this tracking number. Ex. USPS, UPS, FedEx")
    args = parser.parse_args()

    if args.carrier == "usps": 
        url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=" + args.tracking_number
    elif args.carrier == "fedex": 
        url = "https://www.fedex.com/fedextrack/?trknbr=" + args.tracking_number

    html = scrape_url(url)
    tracking_info = filter_html(html, args.carrier)
    # generate_import_data(args.tracking_number, tracking_info, url)

    # session = create_session()
    # print(session)
    # session.close()

