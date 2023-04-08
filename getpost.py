import praw
import random
from PyBay import classify
import json

def fetchSubmission(clientID, clientSecret, subreddit, fetchLimit, minUpvotes, minComments, SORT_TYPE):
    candidates = []
    filtered = []

    # init reddit
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        user_agent="testscript by u/Frostplexx",
    )

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

    # load the json file
    # Load the existing JSON file
    with open("assets/files/produced_videos.json", "r") as f:
        data = json.load(f)
    # weigh them using a classification algorithm
    print("Classifying data...")
    for item in candidates:
        test = classify(item.title)

        if item.id not in data["produced_videos"] and test == "good" and item.score > minUpvotes and item.num_comments > minComments and item.over_18 is False:
            filtered.append(item)
    # sort by score
    filtered.sort(key=lambda x: x.score, reverse=True)
    return filtered


def _fetchComments(chosensubmission, minCommentUpvotes):
    comments = []
    for comment in chosensubmission.comments:
        # skip the MoreComments object
        if isinstance(comment, praw.models.MoreComments):
            continue
        elif comment.id not in comments and comment.score > minCommentUpvotes:
            comments.append(comment)
    return comments
