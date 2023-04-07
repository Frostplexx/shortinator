from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _getDriver(postURL):
    # options
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.desktop-notification", 2)

    # init selenium
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(postURL)
    return driver


def _getWait(driver):
    wait = WebDriverWait(driver, 10)
    return wait


def _takeTitleScreenshot(wait):
    # take the screenshots

    # click the cookie button
    buttonClass = "_1tI68pPnLBjR1iHcL7vsee"
    search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, buttonClass)))
    search.click()

    # wait for the title to load ans take the screenshot
    handle = By.CLASS_NAME
    className = "Post"
    search = wait.until(EC.presence_of_element_located((handle, className)))
    file = open("out/screenshots/title.png", "wb")
    file.write(search.screenshot_as_png)
    file.close()
    return "out/screenshots/title.png"


def _takeCommentScreenshot(wait, comment_id):
    # take the screenshots
    handle = By.ID
    comment_id = "t1_" + comment_id
    search = wait.until(EC.presence_of_element_located((handle, comment_id)))
    fileName = "out/screenshots/comment-" + comment_id + ".png"

    # wait until avatar has loaded
    avatar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2TN8dEgAQbSyKntWpSPYM7")))

    # take the screenshot
    file = open(fileName, "wb")
    file.write(search.screenshot_as_png)
    file.close()

    return fileName


def takeScreenshots(url, comments=None):
    driver = _getDriver(url)
    wait = _getWait(driver)
    _takeTitleScreenshot(wait)
    screenshots = []
    if comments is None:
        pass  # TODO take body screenshot
    else:
        for comment in comments:
            screenshots.append(_takeCommentScreenshot(wait, comment.id))
    driver.close()
    return screenshots
