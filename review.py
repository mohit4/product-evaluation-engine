"""
review.py : Defined a class that will process the review text collectively.
    Currently using textblob and nltk 3.0.
"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.1"   # beta 1
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

# for natural language text processing
import nltk

# Use the below commands to get it
# pip install textblob
# OR
# $ pip install -U textblob
# $ python -m textblob.download_corpora
from textblob import TextBlob as TB

class Review:
    """Review class does all the review processing"""
    def __init__(self,review_text,lang='en'):
        # super(Review, self).__init__()
        # self.arg = arg
        self.text = review_text
        # self.tokens = nltk.word_tokenize(self.text)
        # self.tags = nltk.pos_tag(self.tokens)
        self.tb = TB(self.text)
        # self.language = self.tb.detect_language()
        self.subjectivity = self.tb.subjectivity
        self.polarity = self.tb.polarity

    def get_tokens(self):
        """returns the list of all tokens including punctuations"""
        return [w for w in self.tb.tokens]

    def get_tags(self):
        """return the list of pair of word and pos tag"""
        return [p for p in self.tb.tags]

    def translate(self,from_lang,to_lang=u'en'):
        """translate the current text to specified language"""
        self.tb = self.tb.translate(from_lang,to_lang)

    def get_sentences(self):
        """returns a list of list of pair of words,pos-tag"""
        return [list(TB(str(y)).tags) for y in self.tb.sentences]

    def get_features(self):
        """return a dictionary of noun along with a list of adjectives associated to it"""
        tags = self.get_tags()
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

                # adding the noun features
                if not noun_features.has_key(closest_noun):
                    noun_features[closest_noun] = [tags[i][0]]
                else:
                    noun_features[closest_noun].append(tags[i][0])
        return noun_features
