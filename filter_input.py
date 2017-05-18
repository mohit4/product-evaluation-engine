"""
this file accepts the input from a text file
reviews.txt
and produces an output - filtered.txt
containing a list of tagged words
"""

import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import word_tokenize
import sys
import numpy as np

debugging = True

# these will be used to remove extra words from
stop_words = [
'all', 'just', 'being', 'over', 'both', 'through',
'yourselves', 'its', 'before', 'o', 'herself',
'll', 'had', 'should', 'to', 'only', 'won', 'under',
'ours', 'has', 'do', 'them', 'his', 'very', 'they',
'during', 'now', 'him', 'd', 'did',
'this', 'she', 'each', 'further', 'where',
'few', 'because', 'doing', 'some', 'are',
'our', 'ourselves', 'out', 'what', 'for', 'while',
're', 'does', 'above', 'between', 't',
'be', 'we', 'who', 'were', 'here',
'hers', 'by', 'on', 'about', 'of',
'against', 's', 'or', 'own', 'into',
'yourself', 'down', 'your',
'from', 'her', 'their', 'there', 'been',
'whom', 'too', 'themselves',
'was', 'until', 'more', 'himself', 'that',
'but', 'with', 'than', 'those', 'he',
'me', 'myself', 'ma', 'these', 'up', 'will',
'below', 'can', 'theirs', 'my', 'and',
've', 'then', 'is', 'am', 'it', 'an',
'as', 'itself', 'at', 'have', 'in', 'any', 'if',
'again', 'no', 'when', 'same', 'how', 'other',
'which', 'you', 'shan',
'after', 'most', 'such', 'why', 'a', 'off',
'i', 'm', 'yours', 'so', 'y', 'the', 'having',
'once'
# ,'hadn','not','nor','didn','hasn','mustn','shouldn','couldn','isn','wasn',
# 'aren','wouldn','mightn','weren','don','ain','doesn','needn','haven'
]

"""
Using stored nltk trained model
accepts a list of strings and return a list of list of sentences
I : [r1,r2,r3..rn]
O : [[s1,s2..sn],[s1,s2,..sn]...[s1,s2,..sn]]
"""
def sentence_tokenizer(reviews):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    review_sentences = []
    for review in reviews:
        sents = tokenizer.tokenize(review)
        if debugging:
            print sents
        review_sentences.append(sents)
    return review_sentences

"""
Converts the output generated by sentence_tokenizer to a list of list of list of words
Contains small and stop word filter that filters words smaller than 3
I : [[s1,s2..sn],[s1,s2,..sn]...[s1,s2,..sn]]
I : tokenizer - ['punct','word'] default to word
O : [[[w1,w2..wn],[w1,w2..wn],[w1,w2..wn]],[[w1,w2..wn],[w1,w2..wn],[w1,w2..wn]]...[[w1,w2..wn],[w1,w2..wn]]]

every word w1,w2...wn is a pair that Contains the word and the part-of-speech tag

"""
def sentence_filter(review_sentences,tokenizer='word'):
    # tokenizer used to tokenize based on punctuations
    pwt = WordPunctTokenizer()
    res = []
    for review in review_sentences:
        curr_rev = []
        # working on a single review with list of sentences
        for sent in review_sents:
            if tokenizer=='punct':
                tok_sent = pwt.tokenize(sent)
            else:
                tok_sent = word_tokenize(sent)
            tok_sent = [x.lower() for x in tok_sent if len(x)>=3 and x not in stop_words]   # word filter
            curr_rev.append(nltk.pos_tag(tok_sent)) # added tags
        res.append(curr_rev)
    return res

if __name__ == "__main__":

    if len(sys.argv)>=2:
        filename = sys.argv[1]

    fobj = open(filename,'r')
    reviews = eval(fobj.readline())
    rl = len(reviews)
    fobj.close()

    review_tok = sentence_tokenizer(reviews)
    data = sentence_filter(review_tok)

    fobj = open('filtered_'+filename,'w')
    fobj.write(str(data))
    fobj.close()
