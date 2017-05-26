"""
Processes a review using Review class and stores the result in json file
"""

import os
import json
import sys
from review import Review

debugging = True

def allowed_tag(tag):
    """check if the tag is adjective, noun or adverb"""
    if tag.startswith('JJ') or tag.startswith('NN') or tag.startswith('RB'):
        return True
    return False

def generate_report(review,filename,category):
    """return a dictionary containing the review report"""
    rv = Review(review)
    report = {}
    report["product_id"] = filename.split('.')[0]
    report["category"] = category

    if rv.tb.polarity > 0:
        report["label"] = "pos"
    else:
        report["label"] = "neg"

    report["features"] = rv.get_features()
    report["score"] = rv.tb.polarity
    report["subjectivity"] = rv.tb.subjectivity

    tags = [w for (w,p) in rv.get_tags() if allowed_tag(p)]
    report["keywords"] = tags

    if debugging:
        print "Generated report for :"+report["product_id"]

    return report

if __name__ == "__main__":

    reports = []

    dirname = sys.argv[1]
    if dirname[-1]!='/':
        dirname = dirname + '/'
    filenames = os.listdir(dirname)
    l = len(filenames)
    for i in range(l):
        fobj = open(dirname+filenames[i],'r')
        fobj.readline();fobj.readline()
        reviews = eval(fobj.readline())
        for review in reviews:
            print "[ %.2f %% ] "%(i*100/l),
            reports.append(generate_report(review,filenames[i],"Cell phones and accessories"))
        fobj.close()

    # dump all the reports in json file
    with open('result.json','w') as fp:
        json.dump(reports,fp)
