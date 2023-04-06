import praw
import random
import PyBay

def fetchSubmission(clientID, clientSecret, subreddits, fetchLimit, minUpvotes, minComments):
	candidates = []
	filtered = []

	#init reddit
	reddit = praw.Reddit(
		client_id=clientID,
		client_secret=clientSecret,
		user_agent="testscript by u/Frostplexx",
	)

	#pick a random subreddit from the list
	subreddit = subreddits[random.randint(0, len(subreddits)-1)]
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
		
		if test == "good" and item.score > minUpvotes and item.num_comments > minComments and item.over_18 == False:
			# print(item.title)
			filtered.append(item)
			
	chosensubmission = filtered[random.randint(0, len(filtered)-1)] #TODO update this to not use a random one but the best one
	print("Chosen submission: " + chosensubmission.title)
	return chosensubmission

def fetchComments(chosensubmission, minCommentUpvotes):
	index = 0
	comments = []
	for comment in chosensubmission.comments:
		# skip the MoreComments object 
		if isinstance(comment, praw.models.MoreComments):
			continue
		elif comment.body != "[deleted]" and comment.body != "[removed]" and (len(comment.body) > 10 and len(comment.body) < 100) and comment.author != "AutoModerator" and index <= 10 and comment.id not in comments and comment.score > minCommentUpvotes:
			comments.append(comment)
			index += 1
	return comments
