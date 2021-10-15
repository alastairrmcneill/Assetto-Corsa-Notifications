from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import ACSERVER
import os
import time
from datetime import datetime



# Functions
def convert_text_to_time(time_text):
    time_obj = datetime.strptime(time_text,'%M:%S.%f')
    time_num = time_obj.minute*60 + time_obj.second + float(time_obj.microsecond/1000000)
    return time_num



APPLICATION_PATH = os.path.dirname(__file__)
driver = webdriver.Chrome(APPLICATION_PATH + '/chromedriver')

driver.get('http://149.7.16.11:8840/login')

username_field = driver.find_element_by_id("Username")
password_field = driver.find_element_by_id("Password")

username_field.send_keys(ACSERVER.username)
password_field.send_keys(ACSERVER.password)
password_field.send_keys(Keys.RETURN)

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
        leader = {"Driver": live_best_driver,
                  "Lap time": live_best_time}
    elif offline_best_time_num > live_best_time_num:
        leader = {"Driver": offline_best_driver,
                  "Lap time": offline_best_time}
    else:
        print("There is a tie")
        leader = {}

else:
    print("No time has been set")


message = "The current leader is " + leader["Driver"] + " with a time of " + leader["Lap time"] + "."

print(message)


driver.quit()

