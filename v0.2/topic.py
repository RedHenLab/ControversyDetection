#!/usr/bin/env python


"""
Topic Model v0.2
Author: Nayeem Aquib
Email: nayeemaquib@gmail.com
Date: 06/14/2017

"""

import subprocess
from nltk.tokenize import RegexpTokenizer
# from stop_words import get_stop_words
from gensim import corpora, models
import pyLDAvis.gensim as gensimvis
import pyLDAvis


# bash script to get a month's data(lemmas)
#subprocess.call("bash.sh")

# initialize tokenizer and stopwords
tokenizer = RegexpTokenizer(r'\w+')
en_stop = en_stop = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as',
           'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot',
           'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each',
           'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd",
           "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd",
           "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more',
           'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought',
           'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should',
           "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then',
           'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to',
           'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
           'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's",
           'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself',
           'yourselves', 'apos', 's', 'I', 'will', 'go', 'get', '(', ')', '?', ':', ';', ',', '.', '!', '/', '"', "'", "...",
           "``", "&apos", "&apos;s", "&apos;&apos;"]
stop_chars = ['<', '>']

# get all lemmas between a <story>-</story>-pair:
stories = []
with open('test11.txt') as infile:
    for line in infile:
        l = line.rstrip()
        if l == "<story>":
            story = []
        elif l == "</story>":
            stories.append(story)
            story = []
        elif not any(stop_char in l for stop_char in stop_chars):
            if l not in en_stop:
                story.append(l)

# create dictionary and wordcounts corpus:
dictionary = corpora.Dictionary(stories)
dictionary.save("wordcounts.dict")
print(len(dictionary))
corpus = [dictionary.doc2bow(story) for story in stories]
corpora.MmCorpus.serialize("corpus.mm", corpus)
print(len(corpus))
print(len(stories))

# create tf.idf model:
tfidf_model = models.TfidfModel(corpus)
tfidf_model.save("tfidf_model")
tfidf_corpus = tfidf_model[corpus]
corpora.MmCorpus.serialize("tfidf_corpus.mm", tfidf_corpus)

# create topic model:
#LDA
# LDA
num_topics = 10
lda_model = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=0,
                                     chunksize=2000, passes=20)
lda_model.save("lda_model")
lda_corpus = lda_model[corpus]
corpora.MmCorpus.serialize("lda_corpus.mm", lda_corpus)

print("\nTopics by Latent Dirichlet Allocation model")
topics_found_lda = lda_model.print_topics(num_topics=10, num_words=10)
counter = 1
for t in topics_found_lda:
    print("Topic #{} {}".format(counter, t))
    counter += 1

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.

top_topics = lda_model.top_topics(corpus, num_words=20)
avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
print('Average topic coherence: %.4f.' % avg_topic_coherence)

data_vis_lda = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(data_vis_lda)

print(lda_model.print_topics(num_topics=5, num_words=5))

#LSI
lsi_model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=10) # initialize an LSI transformation
lsi_corpus = lsi_model[tfidf_corpus]
print(lsi_model.print_topics(5, 5))

#HDP
hdp_model = models.hdpmodel.HdpModel(corpus, dictionary, T=30)
hdp_model.save("hdp_model")

print("\nTopics by Hierarchical Dirichlet process model")
topics_found_hdp = hdp_model.print_topics(num_topics=10, num_words=5)
counter = 1
for t in topics_found_hdp:
    print("Topic #{} {}".format(counter, t))
    counter += 1
vis_hdp = gensimvis.prepare(hdp_model, corpus, dictionary)
pyLDAvis.display(vis_hdp)


