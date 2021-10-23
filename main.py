from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import ACSERVER, GOOGLE
import os
import time
import json
import smtplib
from datetime import datetime

# Variables
leader = {'Track': '',
          'Car': '',
          'Driver': '',
          'Lap time': '',
          'Lap time number': -1}

# Functions
def convert_text_to_time(time_text):
    time_obj = datetime.strptime(time_text,'%M:%S.%f')
    time_num = time_obj.minute*60 + time_obj.second + float(time_obj.microsecond/1000000)
    return time_num

def send_email(subject_text):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(GOOGLE.email, GOOGLE.app_password)

        body = ''

        msg = f'Subject: {subject_text} \n\n {body}'

        sender = GOOGLE.email
        receiver = GOOGLE.email

        smtp.sendmail(sender, receiver, msg)



# Gather data
APPLICATION_PATH = os.path.dirname(__file__)
driver = webdriver.Chrome(APPLICATION_PATH + '/chromedriver')

driver.get('http://149.7.16.11:8840/login')

username_field = driver.find_element_by_id("Username")
password_field = driver.find_element_by_id("Password")

username_field.send_keys(ACSERVER.username)
password_field.send_keys(ACSERVER.password)
password_field.send_keys(Keys.RETURN)


# Race info
driver.get("http://149.7.16.11:8840/")

try:
    event = driver.find_element_by_class_name("race-info")
    track = event.find_element_by_xpath("//div[@class='race-info']//strong")
    cars = event.find_elements_by_xpath("//div[@class='race-info']//small")
    car = cars[-1]
    leader['Track'] = track.text
    leader['Car'] = car.text
except:
    print("No event")


# Get timings
driver.get('http://149.7.16.11:8840/live-timing')
time.sleep(1)

# Live best time
try:
    live_table = driver.find_element_by_id("live-table")
    live_best_row = live_table.find_element_by_class_name("driver-row")
    live_best_driver = live_best_row.find_element_by_class_name("driver-link").text
    live_best_time = live_best_row.find_element_by_class_name("best-lap").text
    live_best_time_num = convert_text_to_time(live_best_time)

except:
    live_best_driver = ""
    live_best_time_num = -1

# Disconnected best time
try:
    offline_table = driver.find_element_by_id("live-table-disconnected")
    offline_best_row = offline_table.find_element_by_class_name("driver-row")
    offline_best_driver = offline_best_row.find_element_by_class_name("driver-name").text
    offline_best_time = offline_best_row.find_element_by_class_name("best-lap").text
    offline_best_time_num = convert_text_to_time(offline_best_time)
except:
    offline_best_driver = ""
    offline_best_time_num = -1


# Compare best times

if live_best_time_num > 0 or offline_best_time_num >0:
    if live_best_time_num > offline_best_time_num:
        leader['Driver'] = live_best_driver
        leader['Lap time'] = live_best_time
        leader['Lap time number'] = live_best_time_num

    elif offline_best_time_num > live_best_time_num:
        leader['Driver'] = offline_best_driver
        leader['Lap time'] = offline_best_time
        leader['Lap time number'] = offline_best_time_num

    else:
        print("There is a tie")
        leader = {}

else:
    print("No time has been set")


driver.quit()



# Compare to previous best time
with open('results.json', 'r') as f:
    data = json.load(f)

event = data["Events"][-1]

if event["Track"] == leader["Track"] and event["Car"] == leader["Car"]:
    if leader["Lap time number"] < event["Lap time number"]:
        print("This is a new lap record")

        # Send email
        subject = "The current leader is " + leader["Driver"] + " with a time of " + leader["Lap time"] + "."
        send_email(subject)

        # Update event
        event = leader

        # Update data
        data["Events"][-1] = event

        # Save to json file
        with open('results.json', 'w') as f:
            json.dump(data, f)

else: # It is a new event
    # Send email
    subject = "The current leader is " + leader["Driver"] + " with a time of " + leader["Lap time"] + "."
    send_email(subject)

    data["Events"].append(leader)

    # Save to json file
    with open('results.json', 'w') as f:
        json.dump(data, f)



