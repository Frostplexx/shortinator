import moviepy
from moviepy.editor import *
import random

MARGIN = 40
INBETWEEN_TIME = 0.3

def createClip(screesnhotFile, voiceOverFile):
	audioClip = AudioFileClip(voiceOverFile)
	imageClip = ImageClip(
		screesnhotFile,
		duration=audioClip.duration + INBETWEEN_TIME
	).set_position(("center", "center"))
	imageClip = imageClip.resize(width= (1080 - MARGIN))	
	videoClip = imageClip.set_audio(audioClip)
	videoClip.fps = 1
	return videoClip

def CreateTitleClip():
    
	audioClip = AudioFileClip("out/voiceovers/title.mp3")
	imageClip = ImageClip(
		"out/screenshots/title.png",
		duration=audioClip.duration + INBETWEEN_TIME
	).set_position(("center", "center"))
	imageClip = imageClip.resize(width= (1080 - MARGIN))	
	videoClip = imageClip.set_audio(audioClip)
	videoClip.fps = 1
	return videoClip

def getBackground():
	# load all the files inside assets/clips
	clips = []
	for filename in os.listdir("assets/clips"):
		if filename.endswith(".mp4"):
			clips.append(filename)
	return VideoFileClip(
		"assets/clips/" + clips[random.randint(0, len(clips) - 1)],
		audio=False
	)

def createVideo(commentFiles, voiceOverFiles):
	clips = []
	titleClip = CreateTitleClip()
	clips.append(titleClip)
	
	# loop through the comments and create clips
	for i in range(len(commentFiles)):
		clips.append(createClip(commentFiles[i], voiceOverFiles[i]))
	
	print("Creating final video...")
	for clip in clips:
		if clip.duration == 0:
			exit()
	titleAndComments = concatenate_videoclips(clips).set_position(("center", "center"))
	background = getBackground()
 
	finalVideo = CompositeVideoClip(
		clips=[background, titleAndComments],
		size= background.size
	).set_audio(titleAndComments.audio)
	finalVideo.duration = titleAndComments.duration
	finalVideo.set_fps(background.fps)
 
	outputfile = "out/videos/" + str(random.randint(0, 1000000)) + ".mp4"
	finalVideo.write_videofile(
		outputfile,
		codec="mpeg4",
		threads=8,
		bitrate="5000k",
	)
	return outputfile



