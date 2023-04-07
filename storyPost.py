# this script aims to automatically create youtube shorts by fetching comments from reddit and using them as captions
import gtts
from utils import cleanFolders
from screenshot import takeTitleScreenshot, takeCommentScreenshot, getDriver, getWait
from getpost import fetchSubmission, _fetchComments
from cutter import createVideo, createStoryVideo
import time, math, os, random
from ffmpeg import FFmpeg, Progress
from comments import filterComments

def generateStoryPost(SOTRY_SUBS, FETCH_LIMIT, MIN_UPVOTES, SORT_TYPE, MIN_COMMENTS, MIN_COMMENT_UPVOTES, clientID, clientSecret):
	cleanFolders()
	subreddit = SOTRY_SUBS[random.randint(0, len(SOTRY_SUBS)-1)]

	chosensubmission = fetchSubmission(clientID, clientSecret, subreddit, FETCH_LIMIT, MIN_UPVOTES, MIN_COMMENTS,SORT_TYPE)
 
	tts = gtts.gTTS(chosensubmission.selftext, lang="en", tld="us", slow=False)
	tts.save("out/voiceovers/body.mp3")
	#create a voiceover for the title 
	tts = gtts.gTTS(chosensubmission.title, lang="en", tld="us", slow=False)
	tts.save("out/voiceovers/title.mp3")


	voiceOverFiles = []


	def createVoiceOver(id, text):
		# create voiceover 
		filePath = "out/voiceovers/comment-" + id + ".mp3"
		tts = gtts.gTTS(text, lang="en", tld="us", slow=False)
		tts.save(filePath)
		voiceOverFiles.append(filePath)


	# screenshot the title and the comments

	commentScreenshotFiles = []

	print("Taking screenshots...")
	driver = getDriver(chosensubmission.url)
	wait = getWait(driver)
	takeTitleScreenshot(driver, wait, chosensubmission)
	
	driver.close()
	outfile =  createStoryVideo()

	# remux the video to a mp4 container
	print("Remuxing to mp4...")
	ffmpeg = FFmpeg().option("y").input(outfile).output("out/videos/" + chosensubmission.id + ".mp4")
	ffmpeg.execute()

	# delete the old file
	os.remove(outfile)

	cleanFolders()

	endtime = time.time()
	print("Saved videos as " + chosensubmission.id + ".mp4")
	print("Finished in " + str(math.floor(endtime - starttime)) + " seconds")