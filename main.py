import os
import argparse
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraper import usps_scraper


RDS_USER = os.environ["RDS_USER"]
RDS_PASS = os.environ["RDS_PASS"]
RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_PORT = os.environ["RDS_PORT"]
RDS_DB_NAME = os.environ["RDS_DB_NAME"]


def create_session():
    db_string = (
        f"postgresql://{RDS_USER}:{RDS_PASS}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DB_NAME}"
    )
    db_engine = create_engine(db_string)
    Session = sessionmaker(db_engine)
    session = Session()

    return session


def scrape_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text, "html.parser")

    return html


def filter_html(html, carrier, tracking_number):
    if carrier == "usps":
        tracking_info = usps_scraper.find_tracking_info(html, tracking_number)
        return tracking_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Web scraper that takes your carrier and tracking number, then fetches the tracking history for that package.")
    parser.add_argument("tracking_number", metavar="tracking_number", type=str,
                        help="The tracking number you want to track.")
    parser.add_argument("carrier", metavar="carrier", type=str,
                        help="The shipping carrier that uses this tracking number. Ex. USPS, UPS, FedEx")
    args = parser.parse_args()

    if args.carrier == "usps":
        url = (
            "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1="
            + args.tracking_number
        )
    elif args.carrier == "fedex":
        url = "https://www.fedex.com/fedextrack/?trknbr=" + args.tracking_number

    html = scrape_url(url)
    tracking_info = filter_html(html, args.carrier, args.tracking_number)

    # timezone.convert_timezone_to_utc(
    #     tracking_info["trackingHistory"][0]["date"],
    #     tracking_info["trackingHistory"][0]["location"]
    # )

    # session = create_session()
    # print(session)
    # session.close()
