# this script aims to automatically create youtube shorts by fetching comments from reddit and using them as captions
import gtts
from utils import cleanFolders
from screenshot import takeTitleScreenshot, takeCommentScreenshot, getDriver, getWait
from getpost import fetchSubmission, fetchComments
from cutter import createVideo
import time, math, os, random
from ffmpeg import FFmpeg, Progress
from comments import filterComments
starttime = time.time()

# credentials for reddit
clientID = "ecvNqH1CxmQ8Cls5N0_QNw"
clientSecret = "caMwwkwlu4aS4j8g8oAc4eI-d3b_hQ"

# ----------- user settings -----------
# subreddits = ["askreddit", "truthoffmychest", "showerthoughts", "unsolvedmysteries"]
SUBREDDITS = ["askreddit", "showerthoughts", "ask", "answers", "askmen", "askwomen", "truthoffmychest", "confession", "confessions"]
SOTRY_SUBS = ["truthoffmychest", "confession", "confessions"]
NUMBER_OF_VIDEOS = 1

#post settings 
FETCH_LIMIT = 200
MIN_UPVOTES = 100
# this can be "hot", "new", "top", "controversial", "rising"
SORT_TYPE = "hot"

#comment settings
MIN_COMMENTS = 50
MIN_COMMENT_UPVOTES = 100


# ----------------------------------

# clean the out folder 



def magic():
	cleanFolders()
	subreddit = SUBREDDITS[random.randint(0, len(SUBREDDITS)-1)]

	chosensubmission = fetchSubmission(clientID, clientSecret, subreddit, FETCH_LIMIT, MIN_UPVOTES, MIN_COMMENTS,SORT_TYPE)
 
	if subreddit in SOTRY_SUBS:
		tts = gttts.gTTS(chosensubmission.body, lang="en", tld="us", slow=False)
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

	# get the top 10 comments from the submission
	if subreddit not in SOTRY_SUBS:
		print("Fetching comments...")
		comments = fetchComments(chosensubmission, MIN_COMMENT_UPVOTES)
	
		if comments == []:
			print("No suitable comments found, aborting...")
			exit()

		print("Fetched " + str(len(comments)) + " comments from reddit. Filtering...")
		comments = filterComments(comments)
	
		# alternating use one longer comment and one shorter comment
		oldComments = comments 
		newComments = []
	
		# randomize the order of the comments
		random.shuffle(oldComments)
		
		if len(comments) < 4:
			print("Not enough comments, aborting...")
			exit()
			
		for comment in comments:
			createVoiceOver(comment.id, comment.body)
   
	# screenshot the title and the comments

	commentScreenshotFiles = []

	print("Taking screenshots...")
	driver = getDriver(chosensubmission.url)
	wait = getWait(driver)
	takeTitleScreenshot(driver, wait, chosensubmission)
	if subreddit not in SOTRY_SUBS:
		for comment in comments:
			commentScreenshotFiles.append(takeCommentScreenshot(driver, wait, comment.id))
	
	driver.close()
	if subreddit not in SOTRY_SUBS:
		outfile = createVideo(commentScreenshotFiles, voiceOverFiles)
	else:
		outfile = createStoryVIdeo()

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
 
for i in range(NUMBER_OF_VIDEOS):
	print("Creating video " + str(i+1) + "/" + str(NUMBER_OF_VIDEOS))
	magic()