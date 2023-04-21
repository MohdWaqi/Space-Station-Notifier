import smtplib
import time
from datetime import datetime
import os
from dotenv import load_dotenv

import requests

MY_LAT = 28.838648
MY_LONG = 78.773331
load_dotenv()
MY_KEY = os.environ["KEY"]
ISS_NOTIFY = "http://api.open-notify.org/iss-now.json"
SUN_URL = "https://api.sunrise-sunset.org/json"
EMAIL = "mohdwaqi06@gmail.com"

############### Checking the position of International Space Station #########################


def is_iss_overhead():
    response = requests.get(url=ISS_NOTIFY)
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

############################ Checking if the sky is dark? ###########################


def is_dark():
    parameters = {
        "formatted": 0,
    }

    response = requests.get(SUN_URL, params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

################### Sending mail if its dark and iss is on overhead ######################


while True:
    time.sleep(60)
    if is_iss_overhead() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(EMAIL, MY_KEY)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject: ISS Location\n\nLOOK UP!!!!")
