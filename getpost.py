import praw
import random
import PyBay

def fetchSubmission(clientID, clientSecret, subreddit, fetchLimit, minUpvotes, minComments, SORT_TYPE):
	candidates = []
	filtered = []

	#init reddit
	reddit = praw.Reddit(
		client_id=clientID,
		client_secret=clientSecret,
		user_agent="testscript by u/Frostplexx",
	)

	#pick a random subreddit from the list
	print("Choosing from subreddit: " + subreddit)
	#fetch the top 10 posts from the subreddit
	print("Fetching data...")
 
	if SORT_TYPE == "top":
		print("Sorting by top (day)...")
		for submissions in reddit.subreddit(subreddit).top(limit=fetchLimit, time_filter="day"):
			candidates.append(submissions)
	elif SORT_TYPE == "controversial":
		print("Sorting by controversial...")
		for submissions in reddit.subreddit(subreddit).controversial(limit=fetchLimit):
			candidates.append(submissions)
	elif SORT_TYPE == "new":
		print("Sorting by new...")
		for submissions in reddit.subreddit(subreddit).new(limit=fetchLimit):
			candidates.append(submissions)
	elif SORT_TYPE == "rising":
		print("Sorting by rising...")
		for submissions in reddit.subreddit(subreddit).rising(limit=fetchLimit):
			candidates.append(submissions)
	else:
		print("Sorting by hot...")
		for submissions in reddit.subreddit(subreddit).hot(limit=fetchLimit):
			candidates.append(submissions)

	# weigh them using a classification algorithm
	print("Classifying data...")
	for item in candidates: 
		test = PyBay.classify(item.title)
		
		if test == "good" and item.score > minUpvotes and item.num_comments > minComments and item.over_18 == False:
			# print(item.title)
			filtered.append(item)
			
	chosensubmission = filtered[random.randint(0, len(filtered)-1)] #TODO update this to not use a random one but the best one
	print("Title: " + chosensubmission.title)
	print("URL: " + chosensubmission.url)
	return chosensubmission

def fetchComments(chosensubmission, minCommentUpvotes):
	comments = []
	for comment in chosensubmission.comments:
		# skip the MoreComments object 
		if isinstance(comment, praw.models.MoreComments):
			continue
		elif comment.id not in comments and comment.score > minCommentUpvotes:
			comments.append(comment)
	return comments
