import math
import random, time
import configparser

from comments import getComments
from cutter import createVideo
from getpost import fetchSubmission
from screenshot import takeScreenshots
from utils import cleanFolders, createVoiceOverForTitle, createVoiceOver

# credentials for reddit
config = configparser.ConfigParser()
config.read("settings.ini")

startTime = time.time()
# get videotype from settings.ini
VIDEO_TYPE = config.get("Video Settings", "VIDEO_TYPE")

print("Video type: " + VIDEO_TYPE)

# clean the out folder
cleanFolders()

# get a random subreddit
if VIDEO_TYPE == "story":
    subreddits = config.get("Video Settings", "STORY_SUBS").split(",")
elif VIDEO_TYPE == "ask":
    subreddits = config.get("Video Settings", "ASK_SUBS").split(",")
else:
    print("Invalid video type, aborting...")
    exit()

subreddit = subreddits[random.randint(0, len(subreddits) - 1)]
print("Subreddit: " + subreddit)

# fetch post
fetch_limit = int(config.get("Post Settings", "FETCH_LIMIT"))
min_upvotes = int(config.get("Post Settings", "MIN_UPVOTES"))
min_comments = int(config.get("Comment Settings", "MIN_COMMENTS"))
sort_type = config.get("Post Settings", "SORT_TYPE")
clientID = config.get("Reddit Settings", "CLIENT_ID")
clientSecret = config.get("Reddit Settings", "CLIENT_SECRET")

subs = fetchSubmission(
    clientID,
    clientSecret,
    subreddit,
    fetch_limit,
    min_upvotes,
    min_comments,
    sort_type
)

comments = []
finalSubmission = None
for chosensubmission in subs:
    print("")
    print("Fetched post: " + chosensubmission.title)
    print("URL: " + chosensubmission.url)

    # fetch comments
    comments = getComments(chosensubmission, int(config.get("Comment Settings", "MIN_COMMENT_UPVOTES")))
    if comments is not [] and comments is not None:
        finalSubmission = chosensubmission
        # if there are comments, break the loop
        break

# create voiceovers

# create a voiceover for the title
print("Creating voiceovers")
createVoiceOverForTitle(finalSubmission.title)
voiceOverFiles = []
for comment in comments:
    voiceOverFiles.append(createVoiceOver(comment.id, comment.body))

print("Creating screenshots")
# take screenshots
screenshots = takeScreenshots(finalSubmission.url, comments)
print(screenshots)
print(voiceOverFiles)
title = finalSubmission.title + " #shorts #reddit #" + subreddit
outfile = createVideo(screenshots, voiceOverFiles, title)
cleanFolders()
endTime = time.time()

print("Saved videos as " + finalSubmission.id + ".mp4")
print("Finished in " + str(math.floor(endTime - startTime)) + " seconds")

