"""
extract_sentiment_classified_data.py : this script is used to access the Filtered_Dataset
    and extract and list the pos and neg reviews for training dataset of
    sentiment classifier based on TextBlob
"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.4"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import os
import sys
from textblob import TextBlob as TB

def is_label_positive(reviewText):
    tb = TB(reviewText)
    if tb.polarity >= 0.10:
        return True
    return False

def is_label_subjective(reviewText):
    tb = TB(reviewText)
    if tb.subjectivity >= 0.50:
        return True
    return False

limit = 4000

if __name__ == "__main__":

    # the location of extracted dataset
    dataset_directory = "Filtered_Dataset"

    # the location of classified reviews for model training
    output_directory = "Sentiment_Classifier_Training_Data"

    # in case there is not Filtered_Dataset exit
    if not os.path.exists(dataset_directory):
        print "Filtered_Dataset not found! Please execute amazon_data_extraction_scripts/extract_data.py"
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

        # make directory for current category of products
        if not os.path.exists(output_directory+'/'+dir_name):
            os.mkdir(output_directory+'/'+dir_name)

        # create the list for carrying positive and negative reviews
        pos_reviews = []
        neg_reviews = []

        # controlling the count of positive and negative reviews
        no_of_pos_reviews = 0
        no_of_neg_reviews = 0

        # list all the files within this directory
        filenames = os.listdir(dataset_directory+'/'+dir_name)

        # iterating over filenames
        for filename in filenames:

            # if limit reached no need to extract further
            if no_of_pos_reviews >= limit and no_of_neg_reviews >= limit:
                break

            fobj = open(dataset_directory+'/'+dir_name+'/'+filename,'r')
            # discarding the summary
            fobj.readline()
            # getting current ratings
            ratings = eval(fobj.readline())
            # and the review text
            reviews = eval(fobj.readline())
            no_of_reviews = len(ratings)

            for i in range(no_of_reviews):
                # if the review is objective we don't need it
                if not is_label_subjective(reviews[i]):
                    continue
                # if limit is reached end the process
                if no_of_pos_reviews >= limit and no_of_neg_reviews >= limit:
                    break
                # if the review is positive
                if is_label_positive(reviews[i]) and no_of_pos_reviews<limit:
                    # write the review text into positive reviews and increment the no of pos reviews
                    pos_reviews.append(reviews[i])
                    no_of_pos_reviews+=1
                # otherwise it is negative
                elif no_of_neg_reviews<limit:
                    # write the review text into negative reviews and increment the no of neg reviews
                    neg_reviews.append(reviews[i])
                    no_of_neg_reviews+=1

        # complete the file writing and close the resources
        pos_file = open(output_directory+'/'+dir_name+'/'+'pos_reviews.txt','w')
        pos_file.write(str(pos_reviews))
        pos_file.close()
        neg_file = open(output_directory+'/'+dir_name+'/'+'neg_reviews.txt','w')
        neg_file.write(str(neg_reviews))
        neg_file.close()

        # print appropriate message
        print "Extracted training data for",dir_name
