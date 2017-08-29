#!/usr/bin/env python3

import pandas as pd
import sqlite3

month = input("Which month's stories do you want?(yyyy-mm format e.g.2016-06)\n>")

cnx = sqlite3.connect("%s_stories.db" %(month))
df = pd.read_sql("SELECT * FROM [%s_stories]" %(month), cnx)

sample_size = input("How many stories do you want as a sample?\n>")
sample_stories = df.sample(int(sample_size))

another_cnx = sqlite3.connect("%s_sample_stories.db" %(month))
sample_stories.to_sql("%s_sample_stories" %(month), another_cnx)