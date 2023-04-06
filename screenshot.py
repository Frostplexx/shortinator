from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getDriver(postURL):
	# options
	profile = webdriver.FirefoxProfile()
	profile.set_preference("permissions.default.desktop-notification", 2)

	# init selenium
	driver = webdriver.Firefox(firefox_profile=profile)
	driver.get(postURL)	
	return driver 

def getWait(driver):
	wait = WebDriverWait(driver, 10)
	return wait

def takeTitleScreenshot(driver, wait, chosensubmission):
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

def takeCommentScreenshot(driver, wait, id):
	# take the screenshots
	handle = By.ID
	id = "t1_" + id
	search = wait.until(EC.presence_of_element_located((handle, id)))
	fileName = "out/screenshots/comment-" + id + ".png"
	
	# wait until avatar has loaded
	avatar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2TN8dEgAQbSyKntWpSPYM7")))

	# take the screenshot
	file = open(fileName, "wb")
	file.write(search.screenshot_as_png)
	file.close()
 
	return fileName

