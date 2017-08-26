#!/usr/bin/env python3

import pandas as pd

month = input("Which month's stories do you want?(yyyy-mm format e.g.2016-06)\n>")

df = pd.read_csv("%s_stories.csv" %(month), index_col=0)


keyword = input("Give me the keyword\n>")


def get_story(word):
    stories = df[df["story_itself"].apply(lambda x: word in x)]
    stories.to_csv("keyword_story.csv")
    return stories


get_story(keyword)
