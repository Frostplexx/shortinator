# Shortinator

This program automatically generates shortform videos of reddit posts.

## How it works

1. it chooses a subreddit at random from a list and then its hottes 100 posts
2. the posts are categrozied using naiive bayes
3. one of the "good posts" is selected and the comments are loaded
4. voiceover clips for each comment are being created using google text to speech
5. using selenium we now take screenshots of the post title and the comments
6. everything is combined using moviepy and a background clip from assets/clips is being added

### Requirements

- python3
- pip3
- ffmpeg

Install dependencies using pip

```bash
pip3 install -r requirements.txt
```

## Usage

- Install all the requirements
- Change the settings in main.py to your liking
- Either add your own videos as .mp4 to the assets/clips folder or use the tiktokify.sh script to automatically convert a video to the right size and split it into 50sec long segments
- Only once run `python3 dump_cookies.py` and log in to your google account. Back in the console press enter after you have logged in. This will dump the cookies to a file so that you don't have to log in every time you run the program
- Run `python3 main.py` and wait for the program to finish

## TODO

- [x] make options more obvious
- [x] take upvotes into account for comments
- [ ] not too many short comments
- [x] refractor code
- [ ] fix edgecases
- [ ] auto upload to youtube
- [x] save what posts have been used already
- [ ] build a system that takes youtube analytics as an input for finding good posts