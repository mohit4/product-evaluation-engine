"""
naive_bayes_trainer.py : script used to train the nltk classifier in order to do
    sentiment classification and generate a pickle naive_bayes_classifier
"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.5"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import os
import sys
import re
import operator

import nltk

# managing and removing stopwords
from nltk.corpus import stopwords

# handling sentiment related tasks
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
sentiment_analyzer = SentimentAnalyzer()

# word punctuation tokenizer, it will extract all the punctuations as separate
from nltk.tokenize import WordPunctTokenizer as WPT
wpt = WPT()

# sentence tokenizer using pretrained nltk model
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

contractions = {
"ain't": "are not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I had",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "I had",
"i'd've": "I would have",
"i'll": "I will",
"i'll've": "I will have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it'd": "it had",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they had",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

# for matching the contractions words
contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))

# this will extract the list of features from a document
# returns a dictionary with the given format
# <word1> : True
# <word2> : False
# ...
# <wordn> : True
def document_features(list_of_words,word_features):
    document_words = set(list_of_words)
    features = {}
    for word in word_features:
        features[word]=(word in list_of_words)
    return features

def get_expanded(text,contractions_dict=contractions):
    """accepts the text and return the text with contractions in expanded form"""
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, text.lower())

def filter_doc(doc):
    """remove stopwords from a given doc"""
    discarded = {'no','nor','not'}
    stop = set(stopwords.words('english'))-discarded
    return [[word for word in sent if word not in stop] for sent in doc]

def get_negation(doc):
    """in order to handle the negation add _NEG"""
    return sentiment_analyzer.all_words([mark_negation(sent) for sent in doc])

def get_doc(text):
    """returns a list of lists of words, each word is alpha numeric"""
    return [[x for x in wpt.tokenize(s) if x.isalnum() and len(x)>1] for s in sentence_tokenizer.tokenize(text)]

def remove_small(doc):
    """remove words smaller than equal to 3"""
    res = []
    for w in doc:
        if w.endswith("_NEG") and (len(w)-4)>3:
            res.append(w)
        elif len(w)>3:
            res.append(w)
    return res

def save_classifier(classifier,filename):
    """saving the classifier"""
    f = open(filename+'.pickle','wb')
    pickle.dump(classifier,f)
    f.close()
    print "classifier saved!"

# # for demo purpose only
# dataset_directory = "Sentiment_Classifier_Training_Data"
# dir_name = os.listdir(dataset_directory)[0]
# fobj1 = open(dataset_directory+'/'+dir_name+'/'+'pos_reviews.txt','r')
# pos_reviews = eval(fobj1.readline())
# fobj1.close()
# fobj2 = open(dataset_directory+'/'+dir_name+'/'+'neg_reviews.txt','r')
# neg_reviews = eval(fobj2.readline())
# fobj2.close()

# unigram_feats = sentiment_analyzer.unigram_word_feats(all_words_neg, min_freq=4)

if __name__ == "__main__":

    # printing the formalities
    print "Sentiment classifier trainer (naive bayes classifier) v"+__version__
    print "--------------------------------------------------------------------"
    print "Initializing..."

    # the location of classified reviews for model training
    dataset_directory = "Sentiment_Classifier_Training_Data"

    # the directory where the classifier will be stored
    output_directory = "saved_classifiers"

    # in case there is not Sentiment_Classifier_Training_Data exit
    if not os.path.exists(dataset_directory):
        print "Sentiment_Classifier_Training_Data not found! Please execute classifier_training/extract_sentiment_classified_data.py"
        sys.exit(1)

    # list the name of directories withing the dataset
    # each directory corresponds to a single category of products
    dir_names = os.listdir(dataset_directory)

    # in case there is nothing within the Filtered_Dataset
    if len(dir_names)==0:
        print "No data to process! Exiting."
        sys.exit(1)

    # make appropriate directories in case they don't exists
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # now working on each directory withing the Filtered_Dataset
    for dir_name in dir_names:

        print "fetching reviews for",dir_name[8:-2],

        # fetching positive reviews
        fobj1 = open(dataset_directory+'/'+dir_name+'/'+'pos_reviews.txt','r')
        pos_reviews = eval(fobj1.readline())
        fobj1.close()

        # fetching negative reviews
        fobj2 = open(dataset_directory+'/'+dir_name+'/'+'neg_reviews.txt','r')
        neg_reviews = eval(fobj2.readline())
        fobj2.close()

        print "done"

        print "generating docs...",

        # generating filtered docs
        pos_docs = [( remove_small(get_negation(filter_doc(get_doc(get_expanded(sent))))) ,'pos') for sent in pos_reviews]
        neg_docs = [( remove_small(get_negation(filter_doc(get_doc(get_expanded(sent))))) ,'neg') for sent in neg_reviews]

        # training and testing ratio is 80:20
        training_ratio = 0.80
        pos_ratio = int(training_ratio*len(pos_reviews))
        neg_ratio = int(training_ratio*len(neg_reviews))

        # partitioning the docs into training and testing
        training_docs = pos_docs[:pos_ratio] + neg_docs[:neg_ratio]
        testing_docs = pos_docs[pos_ratio:] + neg_docs[neg_ratio:]

        print "done"

        print "preparing the classifier...",

        # fetching all the words which will make the most_frequent_features.txt
        # all_words_neg = sentiment_analyzer.all_words([w for (w,p) in training_docs])

        # distributing words based on frequency
        word_features = nltk.FreqDist(sentiment_analyzer.all_words([w for (w,p) in training_docs]))

        # then taking the values keys which are most frequent
        word_features  = sorted(word_features.items(),key=operator.itemgetter(1))[-2000:]
        word_features = [x for (x,y) in word_features]

        # generating the feature set based on the word_features
        feature_set = [(document_features(d,word_features),c) for (d,c) in training_docs]

        print "done"

        print "training...",

        # selecting and training the NaiveBayesClassifier from nltk packages
        classifier = NaiveBayesClassifier.train(feature_set)

        print "done"

        print "testing...",

        # generating feature set for testing docs
        feature_set = [(document_features(d,word_features),c) for (d,c) in testing_docs]

        # calculating and printing the accuracy
        acc = nltk.classify.accuracy(classifier, feature_set)
        print "done"

        print "accuracy :",acc

        print "saving classifier..."

        # finally save the classifier in specified location
        save_classifier(classifier,output_directory+'/'+dir_name)

        print "done"

        print "saving features..."

        # also the word features as they'll be required at the time of classification
        fobj = open(output_directory+'/'+dir_name+'_features.txt','w')
        fobj.write(str(word_features))

        print "done"

        print "Classfier generation completed! results are stored in saved_classifiers"
