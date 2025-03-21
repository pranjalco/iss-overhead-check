import requests
from datetime import datetime
import smtplib
import time

"""
# Project 23: ISS Overhead Check

## Author
- **Name**: Pranjal Sarnaik
- **Date**: 04 Jan 2025

## Description
This project checks the position of the International Space Station (ISS) and, if it is overhead during dark hours, sends an automatic email notification to the user. The program utilizes APIs to fetch data and SMTP for email notifications.

### Key APIs Used:
1. **User's Position**: [https://www.latlong.net/](https://www.latlong.net/)
2. **ISS Position**: [http://api.open-notify.org/iss-now.json](http://api.open-notify.org/iss-now.json)
3. **Sunrise and Sunset Times**: [https://api.sunrise-sunset.org/json](https://api.sunrise-sunset.org/json)

### Core Functions:
1. **check_iss_dist()**: Determines if the ISS is within +5 or -5 degrees of the user's latitude and longitude.
2. **is_dark()**: Checks if the environment is dark, as the ISS is only visible during dark hours.

### Features:
- Fetches ISS location and compares it with the user's position.
- Calculates sunrise and sunset times at the user's location.
- Sends an automatic email notification when both conditions (proximity and darkness) are met.
- Continuously checks ISS position every minute.

---

## How to Use:
1. **Get Your Location**: Use [https://www.latlong.net/](https://www.latlong.net/) to find your latitude and longitude.
2. **Replace Values**: Update the `MY_LAT` and `MY_LONG` variables in the code with your latitude and longitude.
3. **Email Configuration**: Replace `MY_EMAIL` and `MY_PASSWORD` with your email and app password.
4. **Run the Program**: Follow the instructions in the "Running the Program" section.

---

## Level
- **Level**: Intermediate
- **Skills**: Python, APIs, SMTP, Automation
- **Domain**: Space & Automation

---

## Features
- Email notifications about ISS visibility overhead.
- Fetches live data from APIs.
- Periodic checks every minute.
- Temporary experimental files are stored in the `experiments` folder.

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/pranjalco/iss-overhead-check.git
   ```
2. Navigate to the project directory:
   ```bash
   cd iss-overhead-check
   ```

---

## Running the Program
1. Ensure Python 3.9 or later is installed on your system.
2. To run the program:
   - **Using PyCharm**: Open the project in PyCharm and run `app.py`.
   - **Using Terminal/Command Prompt**: Navigate to the project folder and execute:
     ```bash
     python app.py
     ```
   - **By Double-Clicking**: You can double-click `app.py` to run it directly, provided Python is set up to execute `.py` files on your system.
3. If the console window closes immediately, run the program from the terminal/command prompt or IDE to see the output.

---

## File Structure
- `app.py`: Main script file.
- `experiments/`: Contains temporary files and practice scripts.

---

**Created by Pranjal Sarnaik**  
*© 2024. All rights reserved.*
"""


def check_iss_dist():
    """This function returns True if ISS is within distance og +5 and -5 of person latitude and longitude"""
    if (MY_LAT + 5) > iss_latitude > (MY_LAT - 5) and (MY_LONG + 5) > iss_longitude > (MY_LONG - 5):
        return True


def is_dark():
    """This function checks if it is dark or not as we can see ISS in dark only"""
    if 8 > hour > 0 or 24 > hour > 16:
        return True


while True:
    MY_EMAIL = "pranjal@gmail.com"
    MY_PASSWORD = "dslfjlkdjlfsdflk"
    MY_MESSAGE = "Subject:ISS\n\nPlease look up"

    # url: https://www.latlong.net/
    MY_LAT = -18  # Your latitude
    MY_LONG = -135  # Your longitude

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # print(f"Iss position \n{MY_LAT, iss_latitude}\n{MY_LONG, iss_longitude}")
    # Your position is within +5 or -5 degrees of the ISS position.

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # print(f"\nSunrise:{sunrise}\nSunset:{sunset}")
    # print(data)

    time_now = datetime.now()
    hour = time_now.hour
    # print(hour)

    if check_iss_dist():
        if is_dark():
            print("Yes! conditions satisfied")
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=MY_MESSAGE)

    time.sleep(60)
