import json

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = selenium.webdriver.Firefox()
driver.get("https://www.youtube.com")
#wait for the user to log in and then save the cookies
input("Please log in and then press enter to save cookies")

cookies = driver.get_cookies()
# save thems as json
with open("assets/files/cookies.json", "w") as f:
    json.dump(cookies, f)

print("Done")