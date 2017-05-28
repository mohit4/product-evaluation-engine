import collections
from textblob import TextBlob as TB
from nltk.corpus import subjectivity
from nltk.metrics import precision,recall,f_measure

import sys
criteria = 0.45
if len(sys.argv)==2:
    criteria = float(sys.argv[1])

n_instances = 4000
subj_docs = [(" ".join(sent),'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(" ".join(sent),'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
print "subj: %d, obj: %d"%(len(subj_docs),len(obj_docs))

train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]
training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats,label) in enumerate(testing_docs):
    refsets[label].add(i)
    observed = "subj" if TB(feats).subjectivity >= criteria else "obj"
    testsets[observed].add(i)

# for subjectives
print "sub precision:",precision(refsets['subj'],testsets['subj'])
print "sub recall:",recall(refsets['subj'],testsets['subj'])
print "sub f-measure:",f_measure(refsets['subj'],testsets['subj'])

# for objectives
print "obj precision:",precision(refsets['obj'],testsets['obj'])
print "obj recall:",recall(refsets['obj'],testsets['obj'])
print "obj f-measure:",f_measure(refsets['obj'],testsets['obj'])
