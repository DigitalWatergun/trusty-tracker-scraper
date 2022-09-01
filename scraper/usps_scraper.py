

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


def findTrackingHistory(html): 
    statusList = html.find("div", class_="panel-actions-content thPanalAction")
    spans = statusList.findAll("span")
    
    spansSorted = []
    start, end = 0, 1
    while end < len(spans): 
        if spans[end].strong: 
            info = spans[start:end]
            cleanInfo = []
            cleanInfo.append(removeWhiteSpace(info[0].strong.text))
            for span in info[1:]: 
                cleanInfo.append(removeWhiteSpace(span.text))
            spansSorted.append(cleanInfo)
            start = end 
        end += 1

    trackingHistory = []
    for item in spansSorted: 
        history = {}
        history["date"] = item[0]
        history["status"] = item[1]
        history["location"] = item[2] if len(item) == 3 else ""
        history["details"] = item[3:] if len(item) > 3 else ""
        trackingHistory.append(history)


    return trackingHistory


def findTrackingInfo(html): 
    trackingInfo = {}
    trackingInfo["eta"] = findEstimatedDelivery(html)
    trackingInfo["trackingHistory"] = findTrackingHistory(html)

    return trackingInfo
