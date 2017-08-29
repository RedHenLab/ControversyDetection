#!/usr/bin/env python3

import pandas as pd
from gensim import corpora, models
import re
import sqlite3

month = input("Which month's lda model do you want to build?(yyyy-mm format e.g.2016-06)\n>")

cnx = sqlite3.connect("%s_stories.db" %(month))
df = pd.read_sql("SELECT * FROM [%s_stories]" %(month), cnx)

lemmas_df = df[df["lemmas"].apply(lambda x: len(eval(x))>=20)] # Getting rid of stories with less than 50 lemmas

print("Length of initial df: %d" %(len(df)))
print("Length of the filtered df: %d" %(len(lemmas_df)))

new_lemmas_df = lemmas_df.reset_index(drop =True) # resetting the index so that it is later easier to concatenate a new df or find data

new_lemmas_df['dates'] = pd.to_datetime(new_lemmas_df['dates']) # Setting up the format of dates column


def windowLdaModel(day1, day3):
    """
    This function takes two inputs, start date and end date, then it builds an lda model for those days' data and concatenate the lda dataframe with the given
    story dataframe
    """
    day1_day3_df = new_lemmas_df[new_lemmas_df["dates"].isin(pd.date_range("2016-01-%s" % (day1), "2016-01-%s" % (day3)))]
    day1_day3_df = day1_day3_df.reset_index(drop=True)
    day1_day3_lemmas = day1_day3_df["lemmas"].tolist()
    day1_day3_new_lemmas = [eval(i) for i in day1_day3_lemmas]
    day1_day3_dictionary = corpora.Dictionary(day1_day3_new_lemmas)
    print("Dictionary Length: %d" % len((day1_day3_dictionary)))
    corpus = [day1_day3_dictionary.doc2bow(story) for story in day1_day3_new_lemmas]
    print("Corpus Length: %d" % (len(corpus)))

    tfidf_model = models.TfidfModel(corpus)  # create tf.idf model
    # tfidf_model.save("tfidf_model")
    tfidf_corpus = tfidf_model[corpus]
    num_topics = 100
    lda_model = models.ldamodel.LdaModel(corpus=tfidf_corpus, id2word=day1_day3_dictionary, num_topics=num_topics,
                                         update_every=0, chunksize=5000, passes=20)
    # lda_model.save("lda_model")
    lda_corpus = lda_model[tfidf_corpus]
    # corpora.MmCorpus.serialize("lda_corpus.mm", lda_corpus)
    # topics_found_lda = lda_model.print_topics(num_topics=5, num_words=10)
    all_topics = lda_model.print_topics(num_topics=100, num_words=10)

    topics = 6*["n/a"] #To match up the length size
    for t in all_topics:
        words = re.findall('"([^"]+)"', t[1])
        words = ' '.join(words)
        topics.append(words)

    lda_df = pd.DataFrame(columns=range(100))

    for i in range(len(day1_day3_new_lemmas)):
        doc = lda_corpus[i]
        for top, prob in doc:
            lda_df.set_value(i, top, prob)

    print(len(topics))

    new_day1_day3_df = pd.concat([day1_day3_df, lda_df], axis=1, join='inner')
    new_day1_day3_df.loc[-1] = topics
    print(new_day1_day3_df.tail())
    new_day1_day3_df.to_csv("%s_%s.csv" % (day1, day3))

    return (new_day1_day3_df, all_topics)

startdate = input("What's the start date?(format: dd e.g. 10)\n >")
enddate = input("What's the end date?(format: dd e.g. 10)\n >")

windowLdaModel(startdate, enddate)

