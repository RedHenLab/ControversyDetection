#!/usr/bin/env python3

import sqlite3
import pandas as pd
from scipy.stats import chi2_contingency

cnx_lda = sqlite3.connect("1_31_LDA.db")
cnx_sentiment = sqlite3.connect("2016-01_sentiments_annotated.db")


# get topic distribution over stories
_ = pd.read_sql("SELECT * FROM [1_31_LDA]", cnx_lda)
topics = [str(i) for i in range(100)]
df_lda = _[topics]
topics_lemmas = _.loc[_.index[-1]][topics]
df_lda.index = _['story_id']
df_lda = df_lda[:-1]


# get emotion vectors
_ = pd.read_sql("SELECT * FROM [2016-01_sentiments_annotated.db]", cnx_sentiment)
df_emotions = _[['negative', 'ambiguous', 'positive']]
df_emotions.index = _['story_id']


def controversy(topic, cutoff_topic=.1, df_emotions=df_emotions, df_lda=df_lda):
    # retrieve all relevant story ids for given topic
    story_ids = list()
    for row in df_lda.iterrows():
        if row[1][topic] is not None:
            if float(row[1][topic]) > cutoff_topic:
                story_ids.append(row[0])
    story_ids = set(story_ids)

    # retrieve all emotions vectors for relevant stories

    emotion_vectors = list()
    for row in df_emotions.iterrows():
        if str(row[0]) in story_ids:
            if row[1].values.sum() > 0:
                emotion_vectors.append(list(row[1].values))

    # calculate divergence
    if len(emotion_vectors) > 2:
        _, p, _, _ = chi2_contingency(emotion_vectors)
        print("topic " + topic + ": controversy score: " + str(1 - p))
        return (1 - p), story_ids
    else:
        print("topic " + topic + ": not enough stories with emotions vectors in that topic")
        return 0, story_ids


# evaluate for each topic
stories = list()
controversy_scores = list()
for topic in topics:
    score, ids = controversy(topic)
    controversy_scores.append(score)
    stories.append(ids)

df_topic_controversy = pd.DataFrame(index=topics)
df_topic_controversy['controversy'] = controversy_scores
df_topic_controversy['lemmas'] = topics_lemmas
df_topic_controversy['story_ids'] = stories
df_topic_controversy.to_csv("January_controversy_scores.csv")
