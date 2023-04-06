
# rank comments
# give points to the comments
# the longer the better 
# upvotes weigh the most
# replies weigh the second most

def filterComments(comments):
	scoredComments = []
	for comment in comments:
		rank = rankComment(comment)
		scoredComments.append((comment, rank))
	# sort the comments by rank
	scoredComments.sort(key=lambda tup: tup[1], reverse=True)
	print("Ranked " + str(len(scoredComments)) +" comments")
	
	#append comments until 130 words are reached
	newComments = []
	words = 0
	for comment in scoredComments:
		words += len(comment[0].body.split(" "))
		newComments.append(comment[0])
		if words >= 130:
			break
	return newComments



def rankComment(comment):
    commentLength = len(comment.body)
    upvotes = comment.score
    replies = len(comment.replies)
    
    # calcualte score 
    score = (commentLength * 0.1) + (upvotes * 0.6) + (replies * 0.2)
    return score