# this script aims to automatically create youtube shorts by fetching comments from reddit and using them as captions
import praw
import random
import PyBay
import gtts
import os, shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# credentials for reddit
clientID = "ecvNqH1CxmQ8Cls5N0_QNw"
clientSecret = "caMwwkwlu4aS4j8g8oAc4eI-d3b_hQ"

# subreddits = ["askreddit", "truthoffmychest", "showerthoughts", "unsolvedmysteries"]
subreddits = ["askreddit"]
fetchLimit = 100

subreddit = subreddits[random.randint(0, len(subreddits)-1)]

# init lists
candidates = []
filtered = []
comments = []

#init reddit
reddit = praw.Reddit(
	client_id=clientID,
 	client_secret=clientSecret,
  	user_agent="testscript by u/Frostplexx",
)

# clean the out folder 
folder = "out/voiceovers/"
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder = "out/screenshots/"
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))




#pick a random subreddit from the list
print("Choosing from subreddit: " + subreddit)

#fetch the top 10 posts from the subreddit
print("Fetching data...")
for submissions in reddit.subreddit(subreddit).hot(limit=fetchLimit):
	candidates.append(submissions)
	# print(submissions.title)

# weigh them using a classification algorithm
print("Classifying data...")
for item in candidates: 
    test = PyBay.classify(item.title)
    if test == "good":
        # print(item.title)
        filtered.append(item)
        
chosensubmission = filtered[random.randint(0, len(filtered)-1)]
print("Chosen submission: " + chosensubmission.title)

#automatically cleary the voiceovers folder


#create a voiceover for the title 
tts = gtts.gTTS(chosensubmission.title, lang="en", tld="us", slow=False)
tts.save("out/voiceovers/title.mp3")

def createVoiceOver(id, text):
	# create voiceover 
	filePath = f"out/voiceovers/comment-{id}.mp3"
	tts = gtts.gTTS(text, lang="en", tld="us", slow=False)
	tts.save(filePath)
	return filePath

# get the top 10 comments from the submission
print("Fetching comments...")

index = 0
for comment in chosensubmission.comments:
    # skip the MoreComments object 
	if isinstance(comment, praw.models.MoreComments):
		continue
	elif comment.body != "[deleted]" and comment.body != "[removed]" and (len(comment.body) > 10 and len(comment.body) < 100) and comment.author != "AutoModerator" and index <= 10:
		# createVoiceOver(comment.id, comment.body)
		comments.append(comment.id)
		index += 1

# take the screenshots
print("Taking screenshots...")
# options
profile = webdriver.FirefoxProfile()
profile.set_preference("permissions.default.desktop-notification", 2)


# init selenium
driver = webdriver.Firefox(firefox_profile=profile)
driver.get(chosensubmission.url)
wait = WebDriverWait(driver, 10)

def takeTitleScreenshot(driver, wait):
	handle = By.CLASS_NAME
	className = "Post"
	search = wait.until(EC.presence_of_element_located((handle, className)))
	file = open("out/screenshots/title.png", "wb")
	file.write(search.screenshot_as_png)
	file.close()

def takeCommentScreenshot(driver, wait, id):
	handle = By.ID
	id = "t1_" + id
	search = wait.until(EC.presence_of_element_located((handle, id)))
	fileName = "out/screenshots/comment-" + id + ".png"
	
	# wait until avatar has loaded
	avatar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2TN8dEgAQbSyKntWpSPYM7")))
 
	file = open(fileName, "wb")
	file.write(search.screenshot_as_png)
	file.close()
	return fileName


takeTitleScreenshot(driver, wait)
# wait 0.5 seconds

# click the cookie button
buttonClass = "_1tI68pPnLBjR1iHcL7vsee"
search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, buttonClass)))
search.click()


for comment in comments:
	takeCommentScreenshot(driver, wait, comment)
 
# close the browser
driver.close()