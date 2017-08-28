# ControversyDetection

This program detects if a story is controversial or not based on sentiment analysis. The sentiment analysis is based on WN-affect. 

## Python Version and Module Requirements:

Python 3.5.2

Python Modules:
1. pandas
2. numpy
3. nltk
4. gensim
5. sqlite3
6. xml.etree.ElementTree
7. subprocess

## Documentation

For now, each scripts run independently to do their designated tasks. When executed each script will ask for user input when needed.

### create_database.py
This script builds a database of metadata and stories from the folders of raw files in vrnewsscape on a monthly basis. It takes the input in `yyyy-mm` format(e.g. `2016-10`)

### get_story.py and get_sample.py
`get_story.py` builds another database of stories based on chosen keywords. It takes the input in `yyyy-mm` format like before, and a keyword input(e.g. "gay"). It will then build a database with only those stories that contain those keywords.
`get_sample.py` builds a database of random samples of stories. The sample size is given by the user as an input.

### emotion.py and wnaffect.py
These two scripts, originally taken from [here](https://github.com/clemtoy/WNAffect), are used to determine the emotions using the resources in Wordnet domain.

### sentiment_analysis_text.py
`'wordnet-1.6', 'wn-domains-3.2'` are needed to run this script. It takes a text file as an input and does a sentiment analysis using WN-Affect resources. Then it can determine if the text written in that file is controversial or not.

### sentiment_analysis_database.py
This script takes an sqlite database as an input and then tags all the stories that are controversial. 

### window_lda_model.py

This script takes two dates as input and then run an LDA model on all the stories between those two dates. It gives out 100 topics and their LDA probability score as output.

### recurrent_topic_jaccard_index.py

**Needs optimization**

Based on the `window_lda_model.py`, it builds a cluster of topics.

## To-Do
- Automate the process of controversy detection. 
- Optimize the model to determine the controversy on a smaller text. 
- Build a web interface.
