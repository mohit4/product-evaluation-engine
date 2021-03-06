"""
review_class.py : Defined a class that will process the review text collectively.
    Currently using textblob and nltk 2.7.
"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.5"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

# essential modules
import re

# for natural language text processing
import nltk

# managing and removing stopwords
from nltk.corpus import stopwords

# for punctuation tokenizer
from nltk.tokenize import WordPunctTokenizer as WPT
wpt = WPT()

# sentence tokenizer using pretrained nltk model
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# handling sentiment related tasks
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
sentiment_analyzer = SentimentAnalyzer()

# Use the below commands to get it
# pip install textblob
# OR
# $ pip install -U textblob
# $ python -m textblob.download_corpora
from textblob import TextBlob as TB

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

class Review:
    """Review class does all the review processing"""
    def __init__(self,review_text,lang='en'):
        # super(Review, self).__init__()
        # self.arg = arg
        self.text = review_text.lower()
        # added expansion by default
        self.set_expanded()
        # added docs for the review
        self.doc = [[x for x in wpt.tokenize(s) if x.isalnum() and len(x)>1] for s in sentence_tokenizer.tokenize(self.text)]
        # added textblob for sentiment values
        self.tb = TB(self.text)
        # self.language = self.tb.detect_language()
        self.subjectivity = self.tb.subjectivity
        self.polarity = self.tb.polarity

    def set_expanded(self, contractions_dict=contractions):
        """accepts the text and return the text with contractions in expanded form"""
        def replace(match):
            return contractions_dict[match.group(0)]
        self.text = contractions_re.sub(replace, self.text)

    def set_negation(self):
        """in order to handle the negation add _NEG"""
        self.doc = sentiment_analyzer.all_words([mark_negation(sent) for sent in self.doc])

    def remove_small(self):
        """remove words smaller than equal to 3 use only after set_negation"""
        res = []
        for w in self.doc:
            if w.endswith("_NEG") and (len(w)-4)>3:
                res.append(w)
            elif len(w)>3:
                res.append(w)
        self.doc = res

    def filter_doc(self):
        """remove stopwords from a given doc use only before set_negation"""
        discarded = {'no','nor','not'}
        stop = set(stopwords.words('english'))-discarded
        self.doc = [[word for word in sent if word not in stop] for sent in self.doc]

    def get_tokens(self):
        """returns the list of all tokens filtered punctuations"""
        tokens = [[x for x in wpt.tokenize(s) if x.isalnum() and len(x)>1] for s in sentence_tokenizer.tokenize(self.text)]
        return tokens

    def get_tags(self):
        """return the list of pair of word and pos tag"""
        tokens = self.get_tokens()
        return [nltk.pos_tag(x) for x in tokens]

    def translate(self,from_lang,to_lang=u'en'):
        """translate the current text to specified language"""
        self.tb = self.tb.translate(from_lang,to_lang)

    def get_sentences(self):
        """returns a list sentences"""
        return [s for s in sentence_tokenizer.tokenize(self.text)]

    def get_features(self):
        """return a dictionary of noun along with a list of adjectives associated to it"""
        # tags = self.get_tags()
        tokens = self.get_tokens()
        words_neg = sentiment_analyzer.all_words([mark_negation(sent) for sent in tokens])
        tokens = [item for sublist in tokens for item in sublist]
        only_tags = [p for (w,p) in nltk.pos_tag(tokens)]
        ln = len(words_neg)
        tags = [(words_neg[i],only_tags[i]) for i in range(ln)]
        noun_features = {}
        l = len(tags)
        for i in range(l):
            if tags[i][1].startswith('JJ'):
                # find the closest noun
                left = i-1
                right = i+1
                while left>=0 and not tags[left][1].startswith('NN'):
                    left-=1
                while right<l and not tags[right][1].startswith('NN'):
                    right+=1
                if i-left <= right-i:
                    cl_n_i = left
                else:
                    cl_n_i = right
                # checking for HAC failure
                if cl_n_i < 0 or cl_n_i >= l:
                    closest_noun = "this_product"
                else:
                    closest_noun = tags[cl_n_i][0]
                    if closest_noun.endswith("_NEG"):
                        closest_noun = closest_noun[:-4]

                # adding the noun features
                if not noun_features.has_key(closest_noun):
                    noun_features[closest_noun] = [tags[i][0]]
                else:
                    noun_features[closest_noun].append(tags[i][0])
        return noun_features
