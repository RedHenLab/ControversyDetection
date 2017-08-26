#!/usr/bin/env python3

from wnaffect import WNAffect
wna = WNAffect('wordnet-1.6/', 'wn-domains-3.2/')
import nltk
from nltk.tokenize import RegexpTokenizer


with open("test_senti.txt", "r") as f:
    text = f.read()
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(text)
story = nltk.pos_tag(tokens)

emotion_story = []
for word, pos in story:
    emo = wna.get_emotion(word, pos)
    if emo == None:
        continue
    else:
        root_emotion = ' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)])
        emotion_story.append(root_emotion)


def emotionScore(story = emotion_story):
    pos, neg, ambi = 0, 0, 0
    for i in emotion_story:
        if 'positive' in i:
            pos += 1
        elif 'negative' in i:
            neg += 1
        elif 'ambiguous' in i:
            ambi += 1
    return(pos, neg, ambi)

emotion_score = emotionScore()
pos, neg, ambi = emotion_score

def result(pos, neg):
    verdict = ""
    if (pos >= 5 and neg >= 5) and (neg-pos <= 10 or neg-pos >= -10):
        verdict = "Controversial"
    elif (pos < 5 or neg < 5):
        verdict = "Not enough Data"
    else:
       verdict = "Not Controversial"
    return verdict
