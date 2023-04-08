from getpost import _fetchComments
import configparser

# rank comments
# give points to the comments
# the longer the better 
# upvotes weigh the most
# replies weigh the second most
def _filterComments(comments):
    scoredComments = []
    for comment in comments:
        rank = _rankComment(comment)
        scoredComments.append((comment, rank))
    # sort the comments by rank
    scoredComments.sort(key=lambda tup: tup[1], reverse=True)
    print(scoredComments)
    # init config
    config = configparser.ConfigParser()
    config.read("settings.ini")

    # choose the comments from the top such that they best fit the word limit
    newComments = []
    words = 0
    word_limit = config.get("Video Settings", "WORD_LIMIT")
    for comment in scoredComments:
        if words + len(comment[0].body.split()) < int(word_limit):
            newComments.append(comment[0])
            words += len(comment[0].body.split())
        else:
            break

    return newComments


def _rankComment(comment):
    commentLength = len(comment.body)
    upvotes = comment.score
    replies = len(comment.replies)

    # calcualte score 
    score = (commentLength * 0.1) + (upvotes * 0.6) + (replies * 0.2)
    return score


def getComments(chosensubmission, min_comment_upvotes):
    # fetch comments
    comments = _fetchComments(chosensubmission, min_comment_upvotes)
    # check if there are comments
    if not comments:
        print("No suitable comments found, retrying...")
        return None
    # filter comments
    return _filterComments(comments)
