import hashlib


def remove_white_space(element):
    return " ".join(element.strip().split())


def generate_id_hash(hash_string):
    hash = hashlib.sha256(str.encode(hash_string))

    return hash.hexdigest()


def find_estimated_delivery(html):
    try:
        eta_list = html.find("div", class_="expected_delivery")
        day_list = eta_list.findAll("em", class_="day")
        month_year_list = eta_list.findAll("span", class_="month_year")
        time_list = eta_list.findAll("strong", class_="time")

        day = day_list[0].text
        month_year = " ".join(remove_white_space(month_year_list[0].text).split(" ")[0:2])
        time = remove_white_space(time_list[0].text).split(" ")[0]

        eta = f"{day} {month_year} by {time}"

        return eta
    except (AttributeError, IndexError) as error:
        return "N/A"


def find_tracking_status(html):
    try:
        status = html.findAll("p", class_="tb-status")
        return status[0].text
    except IndexError:
        status = html.findAll("h3", class_="banner-header")
        return remove_white_space(status[0].text)


def find_tracking_history(html, tracking_number):
    try:
        status_list = html.find("div", class_="tracking-progress-bar-status-container")
        divs = status_list.findAll("div", class_="tb-step current-step")
        divs.extend(status_list.findAll("div", class_="tb-step collapsed"))

        tracking_history = []
        for div in divs:
            history = {}

            date_text = remove_white_space(div.select(".tb-date")[0].text)
            date = " ".join(date_text.split(" ")[0:5])
            date_details = " ".join(date_text.split(" ")[6:])

            history["tracking_id"] = tracking_number
            history["date"] = " ".join(date.split(" ")[0:5])
            history["status_details"] = div.select(".tb-status-detail")[0].text + ". " + date_details
            if div.select(".tb-location"):
                history["location"] = remove_white_space(div.select(".tb-location")[0].text)
            else:
                history["location"] = ""
            history["id"] = generate_id_hash(tracking_number + date + history["status_details"])

            tracking_history.append(history)

        return tracking_history
    except (AttributeError, IndexError):
        return None


def find_tracking_info(html, tracking_number):
    tracking_info = {}
    tracking_info["carrier"] = "usps"
    tracking_info["tracking_id"] = tracking_number
    tracking_info["eta"] = find_estimated_delivery(html)
    tracking_info["status"] = find_tracking_status(html)
    tracking_info["tracking_history"] = find_tracking_history(html, tracking_number)

    return tracking_info
