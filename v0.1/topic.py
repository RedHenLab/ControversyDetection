from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
print(en_stop)
en_stop.extend(['apos', 's', 'I', 'will'])
stop_chars = ['<', '>']


with open('testMain_2016_01_01.txt') as oldfile, open('testFiltered_2016_01_01.txt', 'w') as newfile:
    for line in oldfile:
        if not any(stop_char in line for stop_char in stop_chars): # getting rid of the lines with the xml tags
            newfile.write(line)

print(sum(1 for line in open('testMain_2016_01_01.txt')))
print(sum(1 for line in open('testFiltered_2016_01_01.txt')))

with open("testFiltered_2016_01_01.txt") as myfile:
    data = " ".join(line.rstrip() for line in myfile)
    tokens = tokenizer.tokenize(data)
    stopped_tokens = [i for i in tokens if not i in en_stop]

print(stopped_tokens[1:20])

texts = []
texts.append(stopped_tokens)
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus)

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=0, chunksize=20000, passes=20)

print(lda.print_topics(num_topics=10, num_words=2))


