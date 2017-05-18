"""
this script extracts the potential features of a product and give it score
using the HAC and RankAlgorithm
"""

import nltk
import sys
from nltk.corpus import wordnet

# this is a stored trained model, experiment to improve the performance
# till now it is working fine... TO TOKENIZE SENTENCE
sent_tok = nltk.data.load('tokenizers/punkt/english.pickle')

# this is the word tokenizer
from nltk.tokenize import word_tokenize

# for fetching adjective scores
from nltk.corpus import sentiwordnet as swn

# for lemmatization
from nltk.stem.wordnet import WordNetLemmatizer as WNL
wnl = WNL()

path = '../../Filtered_Dataset/'

def fetch_data(filename):
    fobj = open(path+filename,'r')
    """
    summaries = eval(fobj.readline())
    ratings = eval(fobj.readline())
    reviews = eval(fobj.readline())
    fobj.close()
    return [summaries,ratings,reviews]
    """
    fobj.readline()
    fobj.readline()
    reviews = eval(fobj.readline())
    fobj.close()
    return reviews

# lemmatizes the word with appropriate pos tag
def lemmatization(word,pos):
    wn_pos = get_wordnet_pos(pos)
    if wn_pos=='':
        return word
    return wnl.lemmatize(word,wn_pos)

# sentence is a list of words
# working on a single sentence and lemmatize the words wherever possible
# returns a list of word,pos-tag pair
# def transform(sentence):
#     l = len(sentence)
#     # part of speech tagging
#     tags = nltk.pos_tag(sentence)
#     for i in xrange(l):
#         sentence[i] = (lemmatization(tags[i][0],tags[i][1]),tags[i][1])
#     return sentence

# assistant to lemmatization
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('JJ'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

# this functions returns the index of the closest noun to the given adjective
def closest_noun(sentence,adjective_index):
    i = j = adjective_index
    l = len(sentence)
    while i>=0 and not (sentence[i][1].startswith('NN') or sentence[i][1].startswith('PR')):
        i-=1
    while j<l and not (sentence[j][1].startswith('NN') or sentence[j][1].startswith('PR')):
        j+=1
    # check the absolute distance from the current adjective
    if abs(i-adjective_index) > abs(j-adjective_index):
        return j    # return the smaller distance
    return i

def high_adjective_count(reviews):
    noun_score_map = {}
    for review in reviews:
        # sentences = [transform([x.lower() for x in nltk.word_tokenize(sentence) if len(x)>=3]) for sentence in sent_tok.tokenize(review)]
        for sentence in sentences:
            # for each adj find the closest noun
            l = len(sentence)
            for i in range(l):
                if sentence[i][1].startswith('JJ'):  # if adjective
                    cl_n_i = closest_noun(sentence,i)
                    if cl_n_i >= l or cl_n_i < 0:
                        # HAC failure
                        # handle it by assigning the adjective to product
                        cl_noun = "this_product"
                    else:
                        cl_noun = sentence[cl_n_i][0]
                    # incrementing noun score or making a new entry to it
                    if not noun_score_map.has_key(cl_noun):
                        noun_score_map[cl_noun]=0
                    noun_score_map[cl_noun]+=1
            # taking threshold as average
    threshold = float(sum(noun_score_map.values()))/len(noun_score_map)
    potential_features = {}
    for noun in noun_score_map:
        if noun_score_map[noun] >= threshold:
            potential_features[noun] = noun_score_map[noun]#threshold
            # potential_features[noun] = threshold
    # potential_features = {key:noun_score_map[key] for key in noun_score_map if noun_score_map[key] > threshold}
    return potential_features

# for demo purpose only ... replace it with an effective solution
inversion_words = ['not',"n't",'neither','no','nor',"don't","didn't",'never',"hasn't","haven't","can't","couldn't"]

# adding code for feature ranking algorithm
def rank_features(potential_features,reviews):
    global_noun_scores = {}
    global_noun_adjective_count = {}
    for review in reviews:
        review_noun_scores = {}
        review_noun_adjective_count = {}
        sentences = [transform([x.lower() for x in nltk.word_tokenize(sentence) if len(x)>=3]) for sentence in sent_tok.tokenize(review)]
        for sentence in sentences:
            # maintaining a left context of 2 words
            left_context = []
            sentence_score = 0
            l = len(sentence)
            for i in range(l):
                if sentence[i][1].startswith('J'):  # if adjective
                    try:
                        word = swn.senti_synset(sentence[i][0]+'.a.01')
                        if word.pos_score > word.neg_score():
                            score =  word.pos_score() # sentiwordnet score here
                        else:
                            score = -1 * word.neg_score()
                    except:
                        score = 0.0

                    # maintaining left context
                    if i == 0:
                        left_context = []
                    elif i == 1:
                        left_context = [sentence[0]]
                    else:
                        left_context = [sentence[i-2],sentence[i-1]]

                    for iw in left_context:
                        if iw in inversion_words:
                            score = -1 * score
                            break

                    cl_n_i = closest_noun(sentence,i)
                    if cl_n_i >= l or cl_n_i < 0:
                        cl_noun = "this_product"
                    else:
                        cl_noun = sentence[cl_n_i][0]
                    if not review_noun_scores.has_key(cl_noun):
                        review_noun_scores[cl_noun]=0
                    review_noun_scores[cl_noun]+=1
                    if not review_noun_adjective_count.has_key(cl_noun):
                        review_noun_adjective_count[cl_noun]=0
                    review_noun_adjective_count[cl_noun]+=1

                    if not global_noun_scores.has_key(cl_noun):
                        global_noun_scores[cl_noun]=0
                    global_noun_scores[cl_noun]+=1
                    if not global_noun_adjective_count.has_key(cl_noun):
                        global_noun_adjective_count[cl_noun]=0
                    global_noun_adjective_count[cl_noun]+=1

                    sentence_score += score

        total_score = sum(review_noun_scores.values())
        total_adjectives = sum(review_noun_adjective_count.values())
        avg_score = total_score/total_adjectives
        # if avg_score > 0:
        #     # review is positive
        # else:
        #     # review is negative

    avg_feature_score = {}
    for noun in global_noun_scores:
        avg_feature_score[noun] = global_noun_scores[noun]/global_noun_adjective_count[noun]
    return avg_feature_score
#
# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         filename = sys.argv[1]
#     reviews = fetch_data(filename)
#     pt = high_adjective_count(reviews)
#     print pt
#     print '---'*10
#
#     feature_scores = rank_features(pt,reviews)
#     for i in feature_scores:
#         print i,'-',feature_scores[i]

if __name__ == "__main__":
    dirname = "filtered_demo_files/"
    filenames = os.listdir(dirname)
    flog = open('features_log.txt','w')
    flog.write("{")
    for filename in filenames:

        fobj = open(dirname+filename,'r')
        reviews = eval(fobj.readline())
        fobj.close()
        features = high_adjective_count(reviews)
        flog.write("'%s':%s,"%(filename,str(features)))
    flog.write("'demo':None}")
    flog.close()
