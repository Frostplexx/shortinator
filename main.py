# this script aims to automatically create youtube shorts by fetching comments from reddit and using them as captions
import gtts
from utils import cleanFolders
from screenshot import takeTitleScreenshot, takeCommentScreenshot, getDriver, getWait
from getpost import fetchSubmission, fetchComments


# credentials for reddit
clientID = "ecvNqH1CxmQ8Cls5N0_QNw"
clientSecret = "caMwwkwlu4aS4j8g8oAc4eI-d3b_hQ"

# ----------- user settings -----------
# subreddits = ["askreddit", "truthoffmychest", "showerthoughts", "unsolvedmysteries"]
subreddits = ["askreddit"]
fetchLimit = 200
minUpvotes = 100
minComments = 20
minCommentUpvotes = 100


# clean the out folder 
cleanFolders()

chosensubmission = fetchSubmission(clientID, clientSecret, subreddits, fetchLimit, minUpvotes, minComments)


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
comments = fetchComments(chosensubmission, minCommentUpvotes)

# screenshot the title and the comments
if comments == []:
    print("No suitable comments found, aborting...")
    exit()


print("Taking screenshots...")
driver = getDriver(chosensubmission.url)
wait = getWait(driver)
takeTitleScreenshot(driver, wait, chosensubmission)
for comment in comments:
	takeCommentScreenshot(driver, wait, comment)
 
driver.close()


