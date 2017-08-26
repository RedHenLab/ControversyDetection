#!/usr/bin/env python3

import timeit
import subprocess # For running the shell command
import xml.etree.ElementTree as ET
import re
import pandas as pd
import sqlite3


month = input("Which month's database do you want to build?(yyyy-mm format e.g.2016-06)\n>")

start = timeit.default_timer()

command_1 = 'find %s -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd \'{}\' && rm *.json.gz" \;'%(month)

command_2 = 'find %s -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd \'{}\' && gunzip -c *.gz | cut -f 1,2,3 >> ../../%s_metadata_story_lemma.txt" \;'%(month, month)



subprocess.call(command_1, shell=True) # This is vulnerable to shell injection attack. Have to make sure only authorized people execute this command.



subprocess.call(command_2, shell=True) # This is vulnerable to shell injection attack. Have to make sure only authorized people execute this command.



"""
Getting the meta data in a list and the real words, pos tags, and lemmas in another list
"""

meta_data = []
stories = []
stop_chars = ['<', '>']
with open("%s_metadata_story_lemma.txt" %(month)) as infile:
    for line in infile:
        l = line.rstrip()
        if "<text" in l:
            meta_data.append(l)
        if l == "<story>":
            story = []
        # for i in meta_data:
        #                     text_id = re.search(r'id="([^"]+)"', i).group(1)
        #                     story.append(text_id)
        elif l == "</story>":
            stories.append(story)
        elif not any(stop_char in l for stop_char in stop_chars):
            story.append(l)

"""
Building a column for each text-unit in the <text> tag
"""

cols = ["id", "collection", "file", "date", "year", "month", "day", "time", "duration", "country", "channel", "title", "video_resolution", "video_resolution_original", "language", "recording_location", "original_broadcast_date", "original_broadcast_time", "original_broadcast_timezone", "local_broadcast_date", "local_broadcast_time", "local_broadcast_timezone" ]

data = []

"""
Building a dataframe where each text-unit is a column
"""

for string in meta_data:
    row = []
    tree = ET.fromstring(string + "</text>")  # corrects wrong format

    for col in cols:
        row.append(tree.get(col))
    data.append(row)

df_meta_data = pd.DataFrame(data, columns=cols)

"""
Using re.search to find and separate real_words, pos_tags, and lemmas and then reconstruct them into list of lists where
each sublist contains all the real_words, pos_tags, and lemmas of each story
"""
real_words = [[re.search(r'(.*)\t(.*)\t(.*)', i).group(1) for i in j] for j in stories]
story_itself = [[' '.join(i)] for i in real_words] # Building the story in a human readable format

pos_tags = [[re.search(r'(.*)\t(.*)\t(.*)', i).group(2) for i in j] for j in stories]
lemmas = [[re.search(r'(.*)\t(.*)\t(.*)', i).group(3) for i in j] for j in stories]

cols_for_stories = ["real_words", "story_itself", "pos_tags", "lemmas"]

# Building the dataframe with unique story ids(e.g.1601000001 for the first story of January2016), actual words, stories in human readable format, lemmas
df_stories = pd.DataFrame({'real_words':real_words, 'story_itself':story_itself, 'pos_tags':pos_tags, 'lemmas':lemmas}, columns=cols_for_stories)

storyid_first_part = month[2:4] + month[5:]

df_stories.insert(0, 'story_id', range(int(storyid_first_part + "000001"), int(storyid_first_part + "000001") + len(df_stories)))


df_meta_data.to_csv("%s_metadata.csv" %(month))
df_stories.to_csv("%s_stories.csv" %(month))

cnx1 = sqlite3.connect('%s_metadata.db' %(month))
cnx2 = sqlite3.connect('%s_stories.db' %(month))

df1 = pd.read_csv('%s_metadata.csv' %(month), index_col=0)
df2 = pd.read_csv('%s_stories.csv' %(month), index_col=0)

df1.to_sql('%s_metadata' %(month), cnx1)
df2.to_sql('%s_stories' %(month), cnx2)



stop = timeit.default_timer()

print("Elapsed time: %s" %(stop - start))