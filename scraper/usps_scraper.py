import hashlib


def remove_white_space(element):
    return " ".join(element.strip().split())


def generate_id_hash(hash_string):
    hash = hashlib.sha256(str.encode(hash_string))

    return hash.hexdigest()


def find_estimated_delivery(html):
    # Rewrite function whenever you have a USPS sample of ETA listed
    return "N/A"


def find_tracking_status(html):
    status = html.findAll("p", class_="tb-status")
    return status[0].text


def find_tracking_history(html, tracking_number):
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


def find_tracking_info(html, tracking_number):
    tracking_info = {}
    tracking_info["carrier"] = "usps"
    tracking_info["tracking_id"] = tracking_number
    tracking_info["eta"] = find_estimated_delivery(html)
    tracking_info["status"] = find_tracking_status(html)
    tracking_info["tracking_history"] = find_tracking_history(html, tracking_number)
    # print(tracking_info)

    return tracking_info
