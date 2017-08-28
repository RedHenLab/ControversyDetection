#!/usr/bin/env python3

import pandas as pd

month = input("Which month's stories do you want?(yyyy-mm format e.g.2016-06)\n>")
df = pd.read_csv("%s_stories.csv" %(month), index_col=0)

sample_size = input("How many stories do you want as a sample?\n>")
sample_stories = df.sample(int(sample_size))
sample_stories.to_csv("sample_stories.csv")
