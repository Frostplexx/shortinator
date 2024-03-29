import math
import random, time, json
import configparser

from upload import uploadVideo
from comments import getComments
from cutter import createVideo, playVideo
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
    subreddits,
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
print(comments)
# create a voiceover for the title
print("Creating voiceovers")
createVoiceOverForTitle(finalSubmission.title)
voiceOverFiles = []
for comment in comments:
    voiceOverFiles.append(createVoiceOver(comment.id, comment.body))

print("Creating screenshots")
# take screenshots
screenshots = takeScreenshots(finalSubmission.url, comments)

title = "#shorts #reddit"
outfile = createVideo(screenshots, voiceOverFiles, title)
cleanFolders()
endTime = time.time()

# add the finalsumbission id to assets/files/produced_videos.json

# Load the existing JSON file
with open("assets/files/produced_videos.json", "r") as f:
    data = json.load(f)

# Add the new ID to the list of produced videos
data["produced_videos"].append(finalSubmission.id)

# Write the updated JSON data back to the file
with open("assets/files/produced_videos.json", "w") as f:
    json.dump(data, f)


# open the video and ask the user if they want to upload it
# opent the video in a video player
playVideo(outfile)
print("Do you want to upload the video? (y/n)")
upload = input()
while upload != "y" and upload != "n":
    print("Invalid input, try again")
    upload = input()

if upload == "y":
    # upload the video
    print("Uploading video...")
    uploadVideo(outfile)
else:
    print("Video not uploaded")

print("Finished in " + str(math.floor(endTime - startTime)) + " seconds")

