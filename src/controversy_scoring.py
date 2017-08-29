
import sqlite3
import pandas as pd
import math
from scipy.stats import chisquare

cnx_lda = sqlite3.connect("1_31_LDA.db")
cnx_sentiment = sqlite3.connect("2016-01_probability_sentiment.db")

df_lda = pd.read_sql("SELECT * FROM [1_31_LDA]", cnx_lda)
df_sentiment = pd.read_sql("SELECT * FROM [2016-01_probability_sentiment]", cnx_sentiment)

topics_lemma = df_lda.iloc[-1]
topic_index = input("Give me a topic index\n >")

def chisquare_score(index = topic_index):
    topic10_lst = [[i, a] for i, a in enumerate(df_lda[index]) if a is not None and not ''.join(a.split()).isalpha() and
                  float(a) > 0.1]

    indices10 = [] # indices of the stories from the db_lda > 0.1 in topic0
    lda_score10 = [] # lda score
    for x in topic10_lst:
        indices10.append(x[0])
        lda_score10.append(x[1])
    emotion_lst10 = [] #All the emotion vector collected from stories gotten from the lda_score > 0.1
    for x in indices10:
        emotion = df_sentiment.iloc[x][7]
        emotion_lst10.append(emotion)
    emotion_lst10 = [0 if math.isnan(x) else x for x in emotion_lst10]
    all_emotion_vector10 = df_sentiment['node_vector/subnode_vector'].tolist()
    all_emotion_vector10 = [0 if math.isnan(x) else x for x in all_emotion_vector10]
    mean_value_emotion10 = sum(all_emotion_vector10)/len(all_emotion_vector10)
    result = chisquare(emotion_lst10, mean_value_emotion10)
    print(result)
    return result

chisquare_score(topic_index)