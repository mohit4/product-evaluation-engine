import nltk
import collections
from nltk.metrics import precision,recall,f_measure
from nltk.corpus import subjectivity
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment.util import *
from nltk.sentiment import SentimentAnalyzer

def document_features(list_of_words,feats):
    document_words = set(list_of_words)
    features = {}
    for word in feats:
        features[word] = (word in list_of_words)
    return features

n_instances = 4000
subj_docs = [(sent,'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent,'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
print "subj: %d, obj: %d"%(len(subj_docs),len(obj_docs))

train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]
training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs

sentiment_analyzer = SentimentAnalyzer()
all_words_neg = sentiment_analyzer.all_words([mark_negation(doc) for doc in training_docs])
unigram_feats = sentiment_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
print "Unigram feats:",len(unigram_feats)
sentiment_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

training_set = sentiment_analyzer.apply_features(training_docs)
test_set = sentiment_analyzer.apply_features(testing_docs)

classifier = NaiveBayesClassifier.train(training_set)
# acc = nltk.classify.accuracy(classifier,test_set)
# print "accuracy:",acc
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats,label) in enumerate(test_set):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

# for subjectives
print "sub precision:",precision(refsets['subj'],testsets['subj'])
print "sub recall:",recall(refsets['subj'],testsets['subj'])
# print "sub f-measure:",f_measure(refsets['subj'],testsets['subj'])

# for objectives
print "obj precision:",precision(refsets['obj'],testsets['obj'])
print "obj recall:",recall(refsets['obj'],testsets['obj'])
# print "obj f-measure:",f_measure(refsets['obj'],testsets['obj'])
