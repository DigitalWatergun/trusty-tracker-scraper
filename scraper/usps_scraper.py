

def removeWhiteSpace(element): 
    return " ".join(element.strip().split())


def findEstimatedDelivery(html):
    try: 
        eta = ""
        etaDayElement = html.find("em", class_="day")
        eta += etaDayElement.text

        etaDateElement = html.find("strong", class_="date")
        eta += " " + etaDateElement.text

        etaMonthYearElement = html.find("span", class_="month_year")
        eta += " " + " ".join(etaMonthYearElement.text.strip().split()[0:2])

        etaTimeElement = html.find("strong", class_="time")
        eta += " " + etaTimeElement.text.strip().split()[0]

        return f"Estimated Delivery by: {eta}"
    except: 
        return "No estimated delivery or the package was already delivered"


def findTrackingStatus(html): 
    status = html.findAll("p", class_="tb-status")
    return status[0].text


def findTrackingHistory(html): 
    statusList = html.find("div", class_="tracking-progress-bar-status-container")
    divs = statusList.findAll("div", class_="tb-step current-step")
    divs.extend(statusList.findAll("div", class_="tb-step collapsed"))

    trackingHistory = []
    for div in divs:
        history = {}
    
        history["status_details"] = div.select(".tb-status-detail")[0].text
        if div.select(".tb-location"):
            history["location"] = removeWhiteSpace(div.select(".tb-location")[0].text)
        history["date"] = removeWhiteSpace(div.select(".tb-date")[0].text)

        trackingHistory.append(history)

    return trackingHistory


def findTrackingInfo(html): 
    trackingInfo = {}
    trackingInfo["eta"] = findEstimatedDelivery(html)
    trackingInfo["status"] = findTrackingStatus(html)
    trackingInfo["trackingHistory"] = findTrackingHistory(html)

    return trackingInfo
