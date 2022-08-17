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


def filterHtml(html, carrier): 
    if carrier == "usps": 
        uspsScraper = UspsScraper(html)
        trackingInfo = uspsScraper.findTrackingInfo()
        del uspsScraper
        return trackingInfo


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Web scraper that takes your carrier and tracking number, then fetches the tracking history for that package.")
    parser.add_argument("trackingNumber", metavar="trackingNumber", type=str, help="The tracking number you want to track.")
    parser.add_argument("carrier", metavar="carrier", type=str, help="The shipping carrier that uses this tracking number. Ex. USPS, UPS, FedEx")
    args = parser.parse_args()

    if args.carrier == "usps": 
        url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=" + args.trackingNumber
    elif args.carrier == "fedex": 
        url = "https://www.fedex.com/fedextrack/?trknbr=" + args.trackingNumber

    html = scrapeUrl(url)
    trackingInfo = filterHtml(html, args.carrier)
    print(trackingInfo)

