# Shortinator

This program automatically generates shortform videos of reddit posts.

## How it works

1. it chooses a subreddit at random from a list and then its hottes 100 posts
2. the posts are categrozied using naiive bayes
3. one of the "good posts" is selected and the comments are loaded
4. voiceover clips for each comment are being created using google text to speech
5. using selenium we now take screenshots of the post title and the comments
6. everything is combined using moviepy and a background clip from assets/clips is being added

## Usage

- Install all the requrements
- Change the settings in main.py to your liking
- Either add your own videos as .mp4 to the assets/clips folder or use the tiktokify.sh script to automatically convert a video to the right size and split it into 50sec long segments