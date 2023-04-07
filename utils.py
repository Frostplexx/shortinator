import os, shutil

import gtts


def cleanFolders():
    folder = "out/voiceovers/"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    folder = "out/screenshots/"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def createVoiceOver(comment_id, text):
    # create voiceover
    filePath = "out/voiceovers/comment-" + comment_id + ".mp3"
    tts = gtts.gTTS(text, lang="en", tld="us", slow=False)
    tts.save(filePath)
    return filePath


def createVoiceOverForTitle(title):
    tts = gtts.gTTS(title, lang="en", tld="us", slow=False,)
    tts.save("out/voiceovers/title.mp3")
