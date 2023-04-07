import json


def classify(text) -> str:
    p_spam = 0  # probability that regardless of content the email is spam
    p_nospam = 0  # probability that regardless of content the email is not spam
    spam_amount = 0  # number of spam emails
    nospam_amount = 0  # number of non spam emails

    # collection of spam words and how many times they appear
    spam_words = {}
    # collection of non spam words and how many times they appear
    nospam_words = {}

    # load data from training.json file
    with open('training.json') as data:
        file_contents = data.read()
        training_data = json.loads(file_contents)["data"]

    # calculate p_spam and p_nospam
    for item in training_data:
        item["text"] = item["text"].lower()
        if item["label"] == "good":
            p_spam += 1
            # loop trough each word in the email
            for word in item["text"].split(" "):
                # check if the word is already in the dictionary
                if word in spam_words:
                    # if it is, increment the value
                    spam_words[word] += 1
                else:
                    # if not, add it to the dictionary
                    spam_words[word] = 1
        else:
            p_nospam += 1
            # loop trough each word in the email
            for word in item["text"].split(" "):
                # check if the word is already in the dictionary
                if word in nospam_words:
                    # if it is, increment the value
                    nospam_words[word] += 1
                else:
                    # if not, add it to the dictionary
                    nospam_words[word] = 1

    spam_amount = p_spam
    nospam_amount = p_nospam

    p_spam = p_spam / len(training_data)
    p_nospam = p_nospam / len(training_data)

    # calculate the probability of each word in the spam_words dictionary
    for word in spam_words:
        spam_words[word] = spam_words[word] / spam_amount
    # calculate the probability of each word in the nospam_words dictionary
    for word in nospam_words:
        nospam_words[word] = nospam_words[word] / nospam_amount

    # print("Training complete!")
    # print("-------------------")
    # print("")
    # ask user for input
    email = text
    # print("")
    # calculate the probability that the email is spam

    # make everything lowercase
    email = email.lower()

    # loop trough each word in the email
    for word in email.split(" "):

        # replace . with nothing
        word = word.replace(".", "")
        word = word.replace(":", "")
        word = word.replace(";", "")
        word = word.replace("!", "")
        word = word.replace("?", "")

        # filter out punctuation and new lines
        if word == "\"" or word == "\'" or word == "\n" or word == "." or word == "!" or word == "?" or word == "," or word == ":" or word == ";" or word == "(" or word == ")" or word == "[" or word == "]" or word == "{" or word == "}":
            continue
        # check if the word is already in the dictionary
        if word in spam_words:
            # print("Word: ", word, ", Probability that its spam: ", spam_words[word])
            # if it is, increment the value
            p_spam *= spam_words[word]
        elif word not in spam_words:
            # if not, use the unknown word probability
            p_spam *= 1 / (spam_amount + (len(spam_words) + 1))  # +1 for unknown word
        # print("Unknown word: ", word, ", Probability of it being spam: ", 1 / (spam_amount + (len(spam_words) + 1)))
        if word in nospam_words:
            # print("Word: ", word, ", Probability that its not spam: ", nospam_words[word])
            # if it is, increment the value
            p_nospam *= nospam_words[word]
        elif word not in nospam_words:
            p_nospam *= 1 / (nospam_amount + (len(nospam_words) + 1))  # +1 for unknown word
        # print("Unknown word: ", word, ", Probability of it not being spam: ", 1 / (nospam_amount + (len(
    # nospam_words) + 1)))
    # print(" ")

    # print("Spam vocabulary size: ", len(spam_words))
    # print("Non spam vocabulary size: ", len(nospam_words))
    # print ("p_spam: ", p_spam)
    # print("p_nospam: ", p_nospam)

    print("")
    if p_spam > p_nospam:
        return "good"
    else:
        return "bad"
