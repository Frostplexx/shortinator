import configparser
import json
import praw
from PyBay import classify


def fetchSubmission(clientID, clientSecret, subreddits, fetchLimit, minUpvotes, minComments, SORT_TYPE):
    candidates = []
    filtered = []

    # init reddit
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        user_agent="testscript by u/Frostplexx",
    )

    print("Fetching data, please be patient...")

    if SORT_TYPE == "top":
        print("Sorting by top (day)")
        for subreddit in subreddits:
            print("Gathering data from " + subreddit + "...")
            for submissions in reddit.subreddit(subreddit).top(limit=fetchLimit, time_filter="day"):
                candidates.append(submissions)
    elif SORT_TYPE == "controversial":
        print("Sorting by controversial...")
        for subreddit in subreddits:
            print("Gathering data from " + subreddit + "...")
            for submissions in reddit.subreddit(subreddit).controversial(limit=fetchLimit):
                candidates.append(submissions)
    elif SORT_TYPE == "new":
        print("Sorting by new...")
        for subreddit in subreddits:
            print("Gathering data from " + subreddit + "...")
            for submissions in reddit.subreddit(subreddit).new(limit=fetchLimit):
                candidates.append(submissions)
    elif SORT_TYPE == "rising":
        print("Sorting by rising...")
        for subreddit in subreddits:
            print("Gathering data from " + subreddit + "...")
            for submissions in reddit.subreddit(subreddit).rising(limit=fetchLimit):
                candidates.append(submissions)
    else:
        print("Sorting by hot...")
        for subreddit in subreddits:
            print("Gathering data from " + subreddit + "...")
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

        if item.id not in data[
            "produced_videos"] and test == "good" and item.score > minUpvotes and item.num_comments > minComments and item.over_18 is False:
            filtered.append(item)
    # sort by score

    return _sortPosts(filtered)


def _sortPosts(posts):
    # ranks the posts by score, and amount of comments with different weights, and returns the sorted list without
    # the scores the weights are 0.5 for score and 0.5 for comments
    config = configparser.ConfigParser()
    config.read("settings.ini")
    postUpvoteWeight = float(config.get("Advanced Settings", "POST_UPVOTES_WEIGHT"))
    postCommentWeight = float(config.get("Advanced Settings", "POST_COMMENTS_WEIGHT"))
    return sorted(posts, key=lambda x: (x.score * postUpvoteWeight) + (x.num_comments * postCommentWeight),
                  reverse=True)


def _fetchComments(chosensubmission, minCommentUpvotes):
    comments = []
    for comment in chosensubmission.comments:
        # skip the MoreComments object
        if isinstance(comment, praw.models.MoreComments):
            continue
        elif comment.id not in comments and comment.score > minCommentUpvotes:
            comments.append(comment)
    return comments
