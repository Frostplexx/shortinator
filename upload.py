import configparser
import json
import os
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def uploadVideo(video):
    config = configparser.ConfigParser()
    config.read("settings.ini")

    title = config.get("Video Settings", "VIDEO_TITLE")
    driver = selenium.webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    # load cookies from file
    driver.get("https://youtube.com")
    with open("assets/files/cookies.json", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    # reload the page
    driver.get("https://youtube.com/upload")
    # wait for the page to load
    # upload the video

    # wait for the page to load
    uploadButton = wait.until(EC.presence_of_element_located((By.ID, "select-files-button")))
    # click the upload buttou
    uploadButton.click()
    file_input = driver.find_element(By.XPATH, '//*[@id="content"]/input')
    abs_path = os.path.abspath(video)
    file_input.send_keys(abs_path)
    # wait for the upload button to be clickable

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next-button"]')))
    for i in range(3):
        next_button.click()
        time.sleep(1)

    print("Done")