"""
run this on python3
"""

import sys
import nltk
import collections
from nltk.metrics import precision,recall,f_measure,accuracy
from nltk.corpus import subjectivity
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment.util import *
from nltk.sentiment import SentimentAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as WNL
from nltk.corpus import wordnet
stop = set(stopwords.words('english'))
wnl = WNL()

# sentence is a list of words
# working on a single sentence and lemmatize the words wherever possible
# returns a list of words
def transform(sentence):
    l = len(sentence)
    # part of speech tagging
    tags = nltk.pos_tag(sentence)
    for i in range(l):
        sentence[i] = lemmatization(tags[i][0],tags[i][1])
    return sentence

# lemmatizes the word with appropriate pos tag
def lemmatization(word,pos):
    wn_pos = get_wordnet_pos(pos)
    if wn_pos=='':
        return word
    return wnl.lemmatize(word,wn_pos)

# assistant to lemmatization
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def document_features(list_of_words,feats):
    document_words = set(list_of_words)
    features = {}
    for word in feats:
        features[word] = (word in list_of_words)
    return features

def filter_allowed(words):
    res = []
    for word in words:
        if word.endswith("_NEG"):
            if word[:-4].isalnum() and len(word[:-4])>3:
                res.append(word)
        else:
            if word.isalnum() and len(word)>3:
                res.append(word)

    return res

def filter_stopword(words):
    res = []
    for word in words:
        if word.endswith("_NEG"):
            if word[:-4] not in stop:
                res.append(word)
        else:
            if word not in stop:
                res.append(word)
    return res

# def is_stopword(word):
#     return word in stop
#
# def is_allowed(word):
#     if word.endswith("_NEG") and len(word)-4>3:
#         return True
#     elif len(word)>3:
#         return True
#     return False

no_of_reviews = 4000
subj_docs = [(transform(sent),'subj') for sent in subjectivity.sents(categories='subj')[:no_of_reviews]]
obj_docs = [(transform(sent),'obj') for sent in subjectivity.sents(categories='obj')[:no_of_reviews]]
print("subj: %d, obj: %d"%(len(subj_docs),len(obj_docs)))

partition = int(0.80*no_of_reviews)

train_subj_docs = subj_docs[:partition]
test_subj_docs = subj_docs[partition:]
train_obj_docs = obj_docs[:partition]
test_obj_docs = obj_docs[partition:]

training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs

# applying filters
training_docs = [(filter_stopword(filter_allowed(d)),p) for (d,p) in training_docs]
testing_docs = [(filter_stopword(filter_allowed(d)),p) for (d,p) in testing_docs]

# handling negations
training_docs = [mark_negation(doc) for doc in training_docs]
testing_docs = [mark_negation(doc) for doc in testing_docs]

sentiment_analyzer = SentimentAnalyzer()

all_words_neg = sentiment_analyzer.all_words(training_docs)
unigram_feats = sentiment_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
unigram_feats = unigram_feats[:2000]

# save unigram feats in file
fobj = open("subjective_trainer_unigram_word_removal_feats.txt",'w')
for w in unigram_feats:
    fobj.write(w+"\n")
fobj.close()

# sys.exit(0)

print("Unigram feats:",len(unigram_feats))
sentiment_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

training_set = sentiment_analyzer.apply_features(training_docs)
test_set = sentiment_analyzer.apply_features(testing_docs)

classifier = NaiveBayesClassifier.train(training_set)
acc = nltk.classify.accuracy(classifier,test_set)
print("accuracy:",acc)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats,label) in enumerate(test_set):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

# for subjectives
print("Subjective")
print("---"*6)
print("sub recall:",recall(refsets['subj'],testsets['subj']))
print("sub precision:",precision(refsets['subj'],testsets['subj']))
print("sub f-measure:",f_measure(refsets['subj'],testsets['subj']))

# for objectives
print("Objective")
print("---"*6)
print("obj recall:",recall(refsets['obj'],testsets['obj']))
print("obj precision:",precision(refsets['obj'],testsets['obj']))
print("obj f-measure:",f_measure(refsets['obj'],testsets['obj']))
