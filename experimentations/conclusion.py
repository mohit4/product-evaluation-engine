"""
analyzes the log files and generate a JSON file containing the results.

format of file

{
    "filenames":[file1,file2,...,filen],
    "file1":{
        "label":pos/neg,
        "features":[battery,charger,...,body],
        "battery":{
            "score":45,
            "adjectives":["awesome","great","good"]
        },
        "charger":{
            "worse":10,
            ...
        }
    }
}
"""

import json
import os
import ast

if __name__ == "__main__":

    dirname = "filtered_demo_files/"
    filenames = os.listdir(dirname)

    labels_file = open('labels_log.txt','r')
    features_file = open('features_log.txt','r')

    labels_data = labels_file.readline()
    features_data = features_file.readline()

    labels = ast.literal_eval(labels_data)
    features = ast.literal_eval(features_data)

    labels_file.close()
    features_file.close()

    result = {}

    # added all the filenames
    result["filenames"] = filenames

    for filename in filenames:
        result[filename] = {"label":labels[filename],"features":features[filename].keys()}

    with open('result.json','w') as fp:
        json.dump(result,fp)
