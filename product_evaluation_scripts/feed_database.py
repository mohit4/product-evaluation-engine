"""
feed_database.py : script that uses the generated classifier in earlier stages to classify the
    dataset and generate reports.
"""

# database schema :
#
# collection : reviews
#     {
#         "product_id" : "B00BHAUSE",
#         "category" : "reviews_Cell_Phones_and_Accessories_5",
#         "text" : "good product, i used it for a while ...",
#         "label" : "subjective"/"objective",
#         "subjectivity" : 0.7890,
#
#         # this can be or cannot be present based on the label
#         "sentiment" : "pos",
#         "sentiment_score" : 0.8490
#     }
#
# collection : product
#     {
#         "product_id" : "B00BHAUSE",
#         "category" : "reviews_Cell_Phones_and_Accessories_5",
#         "total_reviews" : 423,
#         "subjective_reviews" : 301,
#         "objective_reviews" : 122,
#         "positive_reviews" : 275,
#         "negative_reviews" : 126,
#         "tags" : ["iphone","camera","working","good"...],
#         "features" : {
#             "battery" : {
#                 "reviews" : ["not working","quality"],
#                 "score" : 0.5678
#             },
#             "camera" : {
#                 "reviews" : ["great","awesome"],
#                 "score" : 0.8680
#             }
#         }
#     }

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.4"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import os
import sys
import pickle
from pprint import pprint

debugging = False

from textblob import TextBlob as TB

# used to access the mongodb database
from pymongo import MongoClient
from review_class import Review

# client to access the database, defaults to localhost:27017
client = MongoClient()

# accessing the database using its name
db = client['mydb']

# drop the previous collections
db.products.drop()
db.reviews.drop()

# accessing the collection
review_collection = db['reviews']
product_collection = db['products']

# reloads the classifier in memory
def load_classifier(pickle_file):
    """reloading the classifier"""
    f = open(pickle_file,'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

# only adjectives, nouns and adverbs are allowed
def allowed_tag(tag):
    """check if the tag is adjective, noun or adverb"""
    if tag.startswith('JJ') or tag.startswith('NN') or tag.startswith('RB'):
        return True
    return False

def remove_neg(list_of_words):
    """transform the words having _NEG as suffix"""
    res = []
    for word in list_of_words:
        if word.endswith("_NEG"):
            res.append("not "+word[:-4])
        else:
            res.append(word)
    return res

def adjust_score(float_value):
    """accept the value between -1 and 1 and return a value between 0 and 10 with adjusted precision"""
    return float("%.2f"%((float_value+1)*5.0))

# document feature extractor for classifier
def document_features(list_of_words,word_features):
    """returns the mapped list of words with true/false values"""
    document_words = set(list_of_words)
    features = {}
    for word in word_features:
        features[word] = (word in list_of_words)
    return features

def word_score(word):
    tb = TB(word)
    return tb.polarity

if __name__ == "__main__":

    # dataset directory
    dataset_directory = "Filtered_Dataset"

    # check if the filtered dataset exists
    if not os.path.exists(dataset_directory):
        print "Filtered_Dataset not found! Please run amazon_data_extraction_scripts/extract_data.py"
        sys.exit(1)

    # otherwise continue
    dirnames = os.listdir(dataset_directory)

    # each directory is made for a specific category of products
    for dirname in dirnames:

        # each directory has its own NaiveBayesClassifier...
        classifier = load_classifier('saved_classifiers/'+dirname+'.pickle')

        # and set of features
        feat_obj = open('saved_classifiers/'+dirname+'_features.txt','r')
        word_features = eval(feat_obj.readline())
        feat_obj.close()

        # list all the files of this directory/product category
        filenames = os.listdir(dataset_directory+'/'+dirname)

        for filename in filenames:

            # access the file
            fobj = open(dataset_directory+'/'+dirname+'/'+filename,'r')
            # discard ratings and summary
            fobj.readline();fobj.readline()
            # fetch only the reviews
            reviews = eval(fobj.readline())

            # close file resource
            fobj.close()

            # creating product report
            product_report = {}

            # adding filename and category to it
            product_report["product_id"] = filename.split('.')[0]
            product_report["category"] = dirname[8:-2]

            # adding other additional data
            product_report["total_reviews"] = 0
            product_report["subjective_reviews"] = 0
            product_report["objective_reviews"] = 0
            product_report["positive_reviews"] = 0
            product_report["negative_reviews"] = 0
            product_report["keywords"] = []
            product_report["features"] = {}

            keywords = []

            # process each of the reviews
            for review in reviews:

                # incrementing total reviews
                product_report["total_reviews"] += 1

                # create a review object class
                rv_obj = Review(review)

                # creating review report
                review_report = {}

                # adding filename and category to it
                review_report["product_id"] = filename.split('.')[0]
                review_report["category"] = dirname[8:-2]

                # preprocessing the data
                rv_obj.filter_doc()
                rv_obj.set_negation()
                rv_obj.remove_small()

                # adding other additional data
                review_report["text"] = rv_obj.text

                # if the review is subjective then do classification on it
                if rv_obj.subjectivity >= 0.50:
                    # incrementing no of subjective reviews
                    product_report["subjective_reviews"] += 1

                    # getting the label and the associated probability
                    feats = document_features(rv_obj.doc,word_features)
                    # review_report["sentiment"] = classifier.classify(feats)
                    # review_report["sentiment_score"] = classifier.classify(feats)
                    review_report["sentiment_score"] = rv_obj.polarity
                    if rv_obj.polarity >= 0.10:
                        review_report["sentiment"] = "pos"
                    else:
                        review_report["sentiment"] = "neg"

                    # increment the positive negative count accordingly
                    if review_report["sentiment"] == "pos":
                        product_report["positive_reviews"] += 1
                    else:
                        product_report["negative_reviews"] += 1
                    review_report["label"] = "subjective"
                else:
                    review_report["label"] = "objective"
                    product_report["objective_reviews"] += 1

                # inserting review values into mongodb database
                review_collection.insert_one(review_report)

                # getting the features from a review
                product_features = rv_obj.get_features()
                # adding this reviews keywords into keywords buffer
                keywords.extend(product_features.keys())

                # if there are any product features
                for k in product_features:
                    if product_report["features"].has_key(k):
                        product_report["features"][k].extend(product_features[k])
                    else:
                        product_report["features"][k]=product_features[k]

            # iterate and redefine the values within the product report
            for feature in product_report["features"]:
                temp = remove_neg(product_report["features"][feature])
                product_report["features"][feature] = {"review":list(set(temp)),"score":adjust_score(word_score(" ".join(temp)))}

            # adding keywords
            product_report["keywords"] = list(set(keywords))

            # inserting the values into mongodb database
            print product_collection.insert_one(product_report)
