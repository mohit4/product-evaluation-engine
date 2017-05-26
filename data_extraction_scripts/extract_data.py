"""
extract_reviews.py : extract all the specified data such as ratings, summaries, reviews etc.

Usage :
    python extract_reviews.py <input_filename> <output_directory>

    e.g. python amazon_data_extraction_scripts/extract_data.py reviews_Cell_Phones_and_Accessories_5.json.gz

Note :
    By default output_directory is assigned as the name of input zip file

"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.4"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import os
import sys
import gzip

def parse(path):
    g = gzip.open(path,'r')
    for l in g:
        yield eval(l)

if __name__ == "__main__":

    # it will only be executed when at least one command line
    # argument is provided which is dataset
    if len(sys.argv) < 2:
        print "Error : No input dataset provided!"
        sys.exit(1)

    # here all of the dataset's data will be stored
    dataset_directory = "Filtered_Dataset/"

    # the zip files downloaded from amazon reviews data
    input_datasets_directory = "amazon_dataset/"

    # list all the input_datasets
    input_datasets = os.listdir(input_datasets_directory)

    # if specified as second command line argument
    # # otherwise use default
    # if len(sys.argv)==3:
    #     output_directory = sys.argv[2]
    # else:
    #     output_directory = input_dataset.split('.')[-3]

    for input_dataset in input_datasets:

        output_directory = input_dataset.split('.')[-3]

        # handling an edge case
        if output_directory[-1]!='/':
            output_directory = output_directory+'/'

        # make directories if not already exists
        if not os.path.exists(dataset_directory):
            os.mkdir(dataset_directory)
        if not os.path.exists(dataset_directory+output_directory):
            os.mkdir(dataset_directory+output_directory)

        # fetching the data from json zip file
        data_gen = parse(input_dataset)

        # a variable to hold the no of products
        count = 0

        # since there is not way to check the end of a generator
        # we use try catch statement. We're done when an exception occurs
        try:
            # fetching data in a single object
            one_object = data_gen.next()
            product_id = one_object['asin']
            ratings = [one_object['overall']]
            reviewTexts = [one_object['reviewText']]
            summaries = [one_object['summary']]

            # continue until not done
            while True:
                one_object = data_gen.next()
                # if the data belongs to the same product
                # keep appending it.
                if one_object['asin'] == product_id:
                    ratings.append(one_object['overall'])
                    reviewTexts.append(one_object['reviewText'])
                    summaries.append(one_object['summary'])
                # otherwise save the previous records in a file
                else:
                    print "Extracted data for",product_id
                    count+=1
                    # create the file named as product id inside the output directory
                    # and put all the data inside that belongs to previous product
                    fobj = open(dataset_directory+output_directory+product_id+'.txt','w')
                    fobj.write("%s\n%s\n%s"%(str(summaries),str(ratings),str(reviewTexts)))
                    fobj.close()

                    # reset the current buffers and set the id to current id
                    ratings = [one_object['overall']]
                    reviewTexts = [one_object['reviewText']]
                    summaries = [one_object['summary']]
                    product_id = one_object['asin']
        except StopIteration:
            # last values will still be in buffer
            # add them to the dataset
            print "Extracted data for",product_id
            count+=1
            fobj = open(dataset_directory+output_directory+product_id+'.txt','w')
            fobj.write("%s\n%s\n%s"%(str(summaries),str(ratings),str(reviewTexts)))
            fobj.close()

        print "Done!"
        print "Total products :",count
