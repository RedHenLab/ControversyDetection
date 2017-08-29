#!/usr/bin/env python3

import timeit
import xml.etree.ElementTree as ET
import re
import pandas as pd
import sqlite3
import subprocess


month = input("Which month's database do you want to build?(yyyy-mm format e.g.2016-06)\n>")

start = timeit.default_timer()

# Subprocess calls to run some commands in shell.
# The commands are unzipping the vrt files and retrieving the metadata and column 1, 2, 3(words, pos tags, lemmas), and putting them into a text file
command_1 = 'find %s -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd \'{}\' && rm *.json.gz" \;'%(month)
command_2 = 'find %s -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd \'{}\' && gunzip -c *.gz | cut -f 1,2,3 >> ../../%s_metadata_story_lemma.txt" \;'%(month, month)
subprocess.call(command_1, shell=True) # This is vulnerable to shell injection attack. Have to make sure only authorized people execute this command.
subprocess.call(command_2, shell=True) # This is vulnerable to shell injection attack. Have to make sure only authorized people execute this command.



# Getting the meta data in a list and the real words, pos tags, and lemmas in another list


def tree2dict(t):
    out = dict()
    for el in t.items():
        out[el[0]] = el[1]
    return out

meta_data = []
stories = []
text_ids = []
dates = []

en_stop = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as',
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
           "``", "&apos", "&apos;s", "&apos;&apos;", "-lsb-", "-rsb-", "-lcb-", "-rcb-", "-lrb-", "-rrb-", "O&apos;MALLEY", "--"]


stop_chars = ['<', '>']
with open("%s_metadata_story_lemma.txt" % (month)) as infile:
    for line in infile:
        l = line.rstrip()
        if "<text" in l:
            tree = ET.fromstring(l + "</text>")  # corrects wrong format
            meta_data.append(l)
            d = tree2dict(tree)
            text_id = d['id']
            date = d['date']   # Getting the date from the metadata
        if l == "<story>":
            story = []
        elif l == "</story>":
            stories.append(story)
            text_ids.append(text_id)      # Getting the text_id fromt he metadata
            dates.append(date)
        elif not any(stop_char in l for stop_char in stop_chars):
            if l not in en_stop:
                story.append(l)


# Building a column for each text-unit in the <text> tag

cols = ["id", "collection", "file", "date", "year", "month", "day", "time", "duration", "country", "channel", "title", "video_resolution", "video_resolution_original", "language", "recording_location", "original_broadcast_date", "original_broadcast_time", "original_broadcast_timezone", "local_broadcast_date", "local_broadcast_time", "local_broadcast_timezone" ]

data = []


# Building a dataframe where each text-unit is a column

for string in meta_data:
    row = []
    tree = ET.fromstring(string + "</text>")  # corrects wrong format
    for col in cols:
        row.append(tree.get(col))
    data.append(row)

df_meta_data = pd.DataFrame(data, columns=cols)


# Using re.search to find and separate real_words, pos_tags, and lemmas and then reconstruct them into list of lists where
# each sublist contains all the real_words, pos_tags, and lemmas of each story

real_words = [[re.search(r'(.*)\t(.*)\t(.*)', i).group(1) for i in j] for j in stories]
story_itself = [[' '.join(i)] for i in real_words] # Building the story in a human readable format

pos_tags = [[re.search(r'(.*)\t(.*)\t(.*)', i).group(2) for i in j] for j in stories]
lemmas = [[re.search(r'(.*)\t(.*)\t(.*)', i).group(3) for i in j] for j in stories]

cols_for_stories = ["story_itself", "pos_tags", "lemmas", "text_ids", "dates"]

# Building the dataframe with unique story ids(e.g.1601000001 for the first story of January2016), actual words, stories in human readable format, lemmas
df_stories = pd.DataFrame({'story_itself':story_itself, 'pos_tags':pos_tags, 'lemmas':lemmas, 'text_ids': text_ids, 'dates': dates}, columns=cols_for_stories)

storyid_first_part = month[2:4] + month[5:]

df_stories.insert(0, 'story_id', range(int(storyid_first_part + "000001"), int(storyid_first_part + "000001") + len(df_stories)))


# Taking them as type str, since sqlite can't take them directly as lists or tuples
df_stories['story_itself'] = df_stories['story_itself'].astype('str')
df_stories['pos_tags'] = df_stories['pos_tags'].astype('str')
df_stories['lemmas'] = df_stories['lemmas'].astype('str')
df_stories['text_ids'] = df_stories['text_ids'].astype('str')
df_stories['dates'] = df_stories['dates'].astype('str')


#df_meta_data.to_csv("%s_metadata.csv" %(month))
#df_stories.to_csv("%s_stories.csv" %(month))

cnx1 = sqlite3.connect('%s_metadata.db' %(month))
cnx2 = sqlite3.connect('%s_stories.db' %(month))

#df1 = pd.read_csv('%s_metadata.csv' %(month), index_col=0)
#df2 = pd.read_csv('%s_stories.csv' %(month), index_col=0)

df_meta_data.to_sql('%s_metadata' %(month), cnx1)
df_stories.to_sql('%s_stories' %(month), cnx2)

cnx1.close()
cnx2.close()


stop = timeit.default_timer()

print("Elapsed time: %s" %(stop - start))
