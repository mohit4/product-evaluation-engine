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
import pickle

debugging = False

# used to access the mongodb database
from pymongo import MongoClient
from review_class import Review

# client to access the database, defaults to localhost:27017
client = MongoClient()

# accessing the database using its name
db = client['mydb']

# accessing the collection
review_collection = db['reviews']
product_collection = db['product']

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

# document feature extractor for classifier
def document_features(list_of_words,word_features):
    """returns the mapped list of words with true/false values"""
    document_words = set(list_of_words)
    features = {}
    for word in word_features:
        features['contains(%s)'%word] = (word in list_of_words)
    return features

def generate_report(report_pack):
    """return a dictionary containing the review report"""

    report["features"] = rv.get_features()
    report["score"] = rv.tb.polarity
    report["subjectivity"] = rv.tb.subjectivity

    tags = [w for (w,p) in rv.get_tags() if allowed_tag(p)]
    report["keywords"] = tags

    if debugging:
        print "Generated report for :"+report["product_id"]

    return report

if __name__ == "__main__":

    # dataset directory
    dataset_directory = "../Filtered_Dataset"

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
        filenames = os.listdir(dataset_directory+'/'+dirname,'r')

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
            product_report["category"] = dirname

            # adding other additional data
            product_report["total_reviews"] = 0
            product_report["subjective_reviews"] = 0
            product_report["objective_reviews"] = 0
            product_report["positive_reviews"] = 0
            product_report["negative_reviews"] = 0
            product_report["keywords"] = []
            product_report["features"] = {}

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
                review_report["category"] = dirname

                # preprocessing the data
                rv_obj.filter_doc()
                rv_obj.set_negation()
                rv_obj.remove_small()

                # adding other additional data
                review_report["text"] = rv_obj.text

                # if the review is subjective then do classification on it
                if rv_obj.subjectivity >= 0.50:
                    # incrementing no of subjective reviews
                    product_report["subjective_reviews"] = 0

                    # getting the label and the associated probability
                    feats = document_features(rv_obj.doc,word_features)
                    review_report["sentiment"] = classifier.classify(feats)
                    review_report["sentiment_score"] = classifier.classify(feats)

                    # increment the positive negative count accordingly
                    if review_report["sentiment"] == "pos":
                        product_report["positive_reviews"] += 1
                    else:
                        product_report["negative_reviews"] += 1
                    review_report["label"] = "subjective"
                else:
                    review_report["label"] = "objective"
                    product_report["objective_reviews"] += 1
