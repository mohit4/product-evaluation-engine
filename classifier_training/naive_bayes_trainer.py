"""
naive_bayes_trainer.py : script used to train the nltk classifier in order to do
    sentiment classification and generate a pickle naive_bayes_classifier
"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.4"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import os
import sys
import re

from nltk.tokenize import WordPunctTokenizer as WPT
wpt = WPT()

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

def get_expanded(text):
    """accepts the text and return the text into expanded form"""
    def replace(match):
        contractions[match.group(0)]
    return contractions_re.sub(replace, text.lower())

def get_tokens(text):
    """returns a list of tokens"""
    tokens = [x for x in wpt.tokenize(text) if x.isalnum()]

if __name__ == "__main__":

    # the location of classified reviews for model training
    dataset_directory = "Sentiment_Classifier_Training_Data"

    # the directory where the classifier will be stored
    output_directory = "classifiers"

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

        # fetching positive reviews
        fobj1 = open(dataset_directory+'/'+dir_name+'/'+'pos_file.txt','r')
        pos_reviews = eval(fobj1.readline())
        fobj1.close()

        # fetching negative reviews
        fobj2 = open(dataset_directory+'/'+dir_name+'/'+'neg_file.txt','r')
        neg_reviews = eval(fobj2.readline())
        fobj2.close()

        #
