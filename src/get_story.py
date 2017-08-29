#!/usr/bin/env python3

import pandas as pd
import sqlite3

month = input("Which month's stories do you want?(yyyy-mm format e.g.2016-06)\n>")

cnx = sqlite3.connect('%s_stories.db' %(month))
df = pd.read_sql("SELECT * FROM [%s_stories]" %(month), cnx)


keyword = input("Give me the keyword\n>")


def get_story(word):
    stories = df[df["story_itself"].apply(lambda x: word in x)]
    cnx = sqlite3.connect("%s_keyword_stories.db" %(month))
    stories.to_sql("%s_keyword_stories" %(month), cnx)
    return stories


get_story(keyword)
