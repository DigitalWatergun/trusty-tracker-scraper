def remove_white_space(element):
    return " ".join(element.strip().split())


def find_estimated_delivery(html):
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


def find_tracking_status(html):
    status = html.findAll("p", class_="tb-status")
    return status[0].text


def find_tracking_history(html):
    status_list = html.find("div", class_="tracking-progress-bar-status-container")
    divs = status_list.findAll("div", class_="tb-step current-step")
    divs.extend(status_list.findAll("div", class_="tb-step collapsed"))

    tracking_history = []
    for div in divs:
        history = {}

        history["date"] = remove_white_space(div.select(".tb-date")[0].text)
        history["status_details"] = div.select(".tb-status-detail")[0].text
        if div.select(".tb-location"):
            history["location"] = remove_white_space(div.select(".tb-location")[0].text)
        else:
            history["location"] = ""

        tracking_history.append(history)

    return tracking_history


def find_tracking_info(html):
    tracking_info = {}
    tracking_info["eta"] = find_estimated_delivery(html)
    tracking_info["status"] = find_tracking_status(html)
    tracking_info["trackingHistory"] = find_tracking_history(html)
    print(tracking_info)

    return tracking_info
