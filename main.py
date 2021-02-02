from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time, sys

#Start the webdriver and connect to the website
driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")
time.sleep(2) # scanning the QR code
wait = WebDriverWait(driver, 60)

#Find the conversation of the required contact
target = 'GROUP GROUP GROUP'
x_arg = '//span[contains(@title,"' + target + '")]'
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
group_title.click()

#Find the text box and send the message
text = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
for character in 'Dit bericht komt van een robot, u mag praten tegen de robot':
  text.send_keys(character)
  time.sleep(0.05)

#Click the send button
send = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
send.click()
time.sleep(2)

#Wait for a reply
msg_xpath = "//span[contains(@title, '/')]"
keep_waiting = True
while keep_waiting:
  try:
    new_message = wait.until(EC.presence_of_element_located((By.XPATH, msg_xpath)))
  except TimeoutException:
    new_message = None
  if new_message:
    sender = new_message.find_element_by_xpath("../../..//span[contains(@title, '')]")
    print(sender.text)
    print(new_message.text)
    keep_waiting = False

for character in 'Ik geloof er niks van! Salut!':
  text.send_keys(character)
  time.sleep(0.05)
send.click()
time.sleep(1)

#Click on options menu for log-out
log = driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[3]')
log.click()
time.sleep(3)

#Find the log-out option and click it
out = driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[3]/span/div/ul/li[6]/div')
out.click()
time.sleep(2)

#Close the webdriver session
driver.quit()
