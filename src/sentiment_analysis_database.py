#!/usr/bin/env python3

import pandas as pd
from wnaffect import WNAffect # 3rd party open source module that mapped WNAffect from WN
import numpy as np
import sqlite3
from textblob import TextBlob

month = input("Which month's database do you want to build?(yyyy-mm format e.g.2016-06)\n>")


df = pd.read_csv('%s_stories.csv' %(month), index_col=0)


stories_df = df[df["lemmas"].apply(lambda x: len(eval(x))>=50)] # Getting rid of stories with less than 50 lemmas
new_stories_df = stories_df.reset_index(drop=True) # resetting index and starting from 0 again

# new_stories_df['date'] = pd.to_datetime(new_stories_df['date'])

# Textblob Polarity Analysis
stories_lst = new_stories_df["story_itself"].tolist()
pos_tag_lst = new_stories_df['pos_tags'].tolist()


def sentimentAnalysis(story):
    # This function takes the words of a story as input and gives a polarity and a subjectivity score as output
    blob = TextBlob(story)
    for sentence in blob.sentences:
        return sentence.sentiment

story_sentiments = [sentimentAnalysis(story) for story in stories_lst]

if len(story_sentiments) == len(new_stories_df):
    stories_emotion_df = new_stories_df

stories_emotion_df["polarity_sentiments(polarity, subjectivity)"] = story_sentiments


# WN-Affect based sentiment analysis

wna = WNAffect('wordnet-1.6/', 'wn-domains-3.2/')

new_lista = [stories_lst[i][2:-2].split() for i in range(len(stories_lst))]
new_listb = [pos_tag_lst[i][2:-2].split("', '") for i in range(len(pos_tag_lst))]

stories_pos_tag_together_list = [list(zip(new_lista[i], new_listb[i])) for i in range(len(stories_lst))]

emotion_stories = []
senti_stories = stories_pos_tag_together_list[:]

for story in senti_stories:
    emotion_story = []
    for word, pos in story:
        emo = wna.get_emotion(word, pos)
        if emo == None:
            continue
        else:
            #             parent = emo.get_level(emo.level - 1)
            #             grandparent = emo.get_level(emo.level - 2)
            #             emotion_story.append(str(grandparent)+" -> "+str(parent)+" -> "+str(emo))
            root_emotion = ' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)])
            emotion_story.append(root_emotion)

    emotion_stories.append(emotion_story)

if len(stories_emotion_df) == len(emotion_stories):
    stories_emotion_df["wordnet_sentiments"] = emotion_stories

emotion_types = ['positive', 'negative', 'ambiguous']

d = {k: stories_emotion_df.wordnet_sentiments.apply(lambda x: ' '.join(x).count(k)) for k in emotion_types}

wordnet_sentiment_df = stories_emotion_df.assign(**d)


wordnet_sentiment_df["controversiality"] = np.where(wordnet_sentiment_df.eval("(positive>=5 & negative>=5) & (negative-positive <= 10 | negative-positive >= -10)"), "controversial", "is not contrversial")
print(wordnet_sentiment_df.shape)


cnx = sqlite3.connect('%s_sentiments_annotated.db' %(month))
wordnet_sentiment_df.to_csv("%s_stories_sentiment_annotated.csv" %(month))
df_sentiment = pd.read_csv('%s_stories_sentiment_annotated.csv' %(month), index_col=0 )
df_sentiment.to_sql('%s_sentiments_annotated.db' %(month), cnx)

