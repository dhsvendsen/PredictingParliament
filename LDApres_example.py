from OdaGetter import *
from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import nltk.corpus
import sys
from pprint import PrettyPrinter as pp


def get_resumes():
	getter = OdaGetter()

	resumes =  [sag['resume'].replace('\n', ' ') for sag in getter.get_LB_sager() 
					if len(sag['resume']) > 10]

	with open('LDApres_mycorpus.txt', 'w') as outfile:
		for resume in resumes[:-1]:
			outfile.write(resume.encode('utf-8')+'\n')


def get_specific_resume(_id):
	resumes = []
	with open('LDApres_mycorpus.txt', 'r') as infile:
		for line in infile:
			resumes.append(str(line))

	return resumes[_id]


def get_test_resume():
	getter = OdaGetter()

	resumes =  [sag['resume'] for sag in getter.get_LB_sager() 
					if len(sag['resume']) > 10]

	return resumes[-1:]


class MyCorpus(object):
    def __iter__(self):
        for line in open('LDApres_mycorpus.txt'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())


stoplist = nltk.corpus.stopwords.words('danish')

#--> Generate dictionary
dictionary = corpora.Dictionary(simple_preprocess(line) for line in open('LDApres_mycorpus.txt'))
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
			if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()


#--> Initiate corpus iterator
corpus = MyCorpus()

#--> Transform corpus
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#--> Define LDA vector space
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=4)

#--> Get query text and BOW it and transform it to LDA space
with open('LDApres_query.txt', 'r') as infile:
	query_doc = infile.read()

vec_bow = dictionary.doc2bow(simple_preprocess(query_doc))
vec_lda = lda[vec_bow]

#--> Transform BOW representation of corpus to LDA space
corpus_lda = lda[corpus_tfidf]
corpus_lda_mem = []
for doc in corpus_lda:
	corpus_lda_mem.append(doc)

index = similarities.MatrixSimilarity(lda[corpus_lda_mem])


#--> Make the query
sims = index[vec_lda]
ranked_matches = sorted(enumerate(sims), key=lambda item: -item[1])
pp(indent=1).pprint(ranked_matches)

print "\n\n---QUERIED RESUME---\n\n", query_doc

print "\n\n#1 match in corpus:\n\n", get_specific_resume(ranked_matches[0][0])

print "\n\n#2 match in corpus:\n\n", get_specific_resume(ranked_matches[1][0])

print "\n\n#3 match in corpus:\n\n", get_specific_resume(ranked_matches[2][0])










