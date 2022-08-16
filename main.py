import requests
import argparse
from bs4 import BeautifulSoup
from scraper.usps_scraper import UspsScraper
from scraper.fedex_scraper import FedExScraper


def scrapeUrl(url): 
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text, "html.parser")
    
    return html


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Web scraper that takes your carrier and tracking number, then fetches the tracking history for that package.")
    parser.add_argument("trackingNumber", metavar="trackingNumber", type=str, help="The tracking number you want to track.")
    parser.add_argument("carrier", metavar="carrier", type=str, help="The shipping carrier that uses this tracking number. Ex. USPS, UPS, FedEx")
    args = parser.parse_args()

    url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=" + args.trackingNumber
    html = scrapeUrl(url)

    uspsScraper = UspsScraper(html)
    eta = uspsScraper.findEstimatedDelivery()
    print(eta)
    uspsScraper.findTrackingHistory()
