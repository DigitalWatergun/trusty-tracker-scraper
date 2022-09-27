from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz


def convert_date_to_naive(date):
    month_dict = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    date_array = date.replace(",", "").split()
    year = date_array[2]
    month = month_dict[date_array[0]]
    day = date_array[1] if len(date_array[1]) == 2 else "0" + date_array[1]
    hour = date_array[3].split(":")[0]
    minute = date_array[3].split(":")[1]
    if date_array[-1] == "pm":
        hour = str(int(hour) + 12)

    return f"{year}-{month}-{day} {hour}:{minute}"


def find_tracking_timezone(location):
    geolocator = Nominatim(user_agent="TrustyTracker")
    src_location = geolocator.geocode(location)

    tz_finder = TimezoneFinder()
    src_timezone = tz_finder.timezone_at(
        lng=src_location.longitude, lat=src_location.latitude)

    return src_timezone


def convert_timezone_to_utc(date, location):
    local_timezone_str = find_tracking_timezone(location)
    local_timezone = pytz.timezone(local_timezone_str)

    date_object_str = convert_date_to_naive(date)
    naive_datetime = datetime.strptime(date_object_str, "%Y-%m-%d %H:%M")
    local_dt = local_timezone.localize(naive_datetime, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    utc_dt.strftime("%Y-%m-%d %H:%M:%S")
    print(utc_dt)
