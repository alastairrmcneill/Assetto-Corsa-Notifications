from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import username, password
import os
import time


APPLICATION_PATH = os.path.dirname(__file__)
driver = webdriver.Chrome(APPLICATION_PATH + '/chromedriver')

driver.get('http://149.7.16.11:8840/login')

username_field = driver.find_element_by_id("Username")
password_field = driver.find_element_by_id("Password")

username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

driver.get('http://149.7.16.11:8840/live-timing')
time.sleep(1)

table = driver.find_element_by_id("live-table-disconnected")

best_row = table.find_element_by_class_name("driver-row")
best_driver = best_row.find_element_by_class_name("driver-name")
best_lap = best_row.find_element_by_class_name("best-lap")

print(best_driver.text)
print(best_lap.text)

driver.quit()