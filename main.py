from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from signald import Signal
import os

import time
import sys
import json

with open('credentials.txt', 'r') as f:
    credentials = json.load(f)

# Start the webdriver and connect to the website
driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")
time.sleep(2) # scanning the QR code
wait = WebDriverWait(driver, 60)

# Find the conversation of the required contact
x_arg = '//span[contains(@title,"' + credentials['whatsapp-group'] + '")]'
wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
clicked = False
while not clicked:
    try:
        group_title = driver.find_element_by_xpath(x_arg)
        group_title.click()
        clicked = True
    except StaleElementReferenceException as e:
        pass

# # Find the text box and send the message
# text = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
# for character in 'Dit bericht komt van een robot, u mag praten tegen de robot':
#   text.send_keys(character)
#   time.sleep(0.05)
#
# # Click the send button
# send = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
# send.click()
# time.sleep(2)

s = Signal(credentials['signal-account'])

# get screenshots from all received whatsapp messages
# first fetch all old messages
existing_elements = set()
message_elements = driver.find_elements_by_xpath('//*[contains(@class,"message-in")]')
for element in message_elements:
    existing_elements.add(element.get_attribute('data-id'))
# keep waiting for new messages...
while True:
    message_elements = driver.find_elements_by_xpath('//*[contains(@class,"message-in")]')
    for element in message_elements:
        message_id = element.get_attribute('data-id')
        if message_id not in existing_elements:
            existing_elements.add(message_id)
            time.sleep(5)
            balloon_element = element.find_element_by_tag_name('div')
            filename = os.path.abspath(f'data/msg{len(existing_elements):04d}.png')
            with open(filename, 'wb') as file:
                file.write(balloon_element.screenshot_as_png)
            s.send_group_message(credentials['signal-group'], block=True, attachments=[filename])
    time.sleep(1)
