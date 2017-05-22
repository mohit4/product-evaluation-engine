"""
extract_sentiment_classified_data.py : this script is used to access the Filtered_Dataset
    and extract and list the pos and neg reviews based on that
"""

# Credits
__author__ = "Mohit Kumar"
__version__ = "0.9.4"
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import os
import sys

if __name__ == "__main__":

    # the location of extracted dataset
    dataset_directory = "../Filtered_Dataset/"

    # in case there is not Filtered_Dataset exit
    if not os.path.exists(dataset_directory):
        print "Filtered_Dataset not found! Please execute amazon_data_extraction_scripts/extract_data.py"
        sys.exit(1)

    # list the name of directories withing the dataset
    dir_names = os.listdir(dataset_directory)

    # in case there is nothing within the Filtered_Dataset
    if len(dir_names)==0:
        print "No data to process! Exiting."
        sys.exit(1)
