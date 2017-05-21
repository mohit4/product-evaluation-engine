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
        self.tags = tb.tags
        self.language = tb.detect_language()
        self.subjectivity = tb.subjectivity
        self.polarity = tb.polarity

    def get_tokens(self):
        """returns the list of all tokens including punctuations"""
        return [w for w in self.tb.tokens]

    def get_tags(self):
        """return the list of pair of word and pos tag"""
        return [p for p in self.tags]

    def translate(self,from_lang,to_lang=u'en'):
        """translate the current text to specified language"""
        self.tb = self.tb.translate(from_lang,to_lang)
