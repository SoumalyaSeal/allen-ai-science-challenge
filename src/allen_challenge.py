from corpus_indexing import check_lucene_index, lucene_retriever
from question_analysis import read_training
from feature_extraction import retrieval_score_feature,freq_dist, similarity_feature, w2v_feature, google_dis_feature
from utils import *
from answer_ranking_perceptron import *
import time, pickle


slim_flag = True  # if True: only use Noun, Verb, Adj+Adv


# check lucene index
index_begin_time = time.time()
check_lucene_index()
index_end_time = time.time()
print "Total indexing time:{}".format(index_end_time-index_begin_time)


# read questions
# get questions / correct answer / answers

training_path = '../data/training/training_set.tsv'
_, cor, ans = read_training(training_path)  # questions, correct answer, answers

# questions (pos tag added) will read directly from binary file
questions_pos_path = '../data/questions_pos'
with open(questions_pos_path, 'rb') as f:
    que = pickle.load(f)

for query_string in que:
    query_slim = get_VNA(query_string, keepV=False, keepN=True, keepA=True)  # keep verb, noun and adj+adv
    query_slim = " ".join(query_slim)
    if slim_flag and query_slim != '':
        res = lucene_retriever(query_slim, use_BM25=True)
    else:
        query = ' '.join([i[0] for i in query_string])
        res = lucene_retriever(query, use_BM25=True)  # if don't wanna handle questions, start here
    corpus_names, DocIDs, scores, texts = [], [], [], []
    for r in res:
        corpus_names.append(r[0])
        DocIDs.append(r[1])
        scores.append(r[2])
        texts.append(r[3])


# retrieval feature
path_retrieval_feature = '../data/retrieval_feature'
if check_score_exist(path_retrieval_feature):
    rs_retrieval = load_feature_score(path_retrieval_feature)
else:
    rs_retrieval = retrieval_score_feature(texts, ans)
    dump_feature_score(path_retrieval_feature, rs_retrieval)


# use similarity feature: count # of words
path_similarity_feature = '../data/similarity_feature'
if check_score_exist(path_similarity_feature):
    rs_similarity = load_feature_score(path_similarity_feature)
else:
    od = freq_dist(texts)
    rs_similarity = similarity_feature(od, ans)
    dump_feature_score(path_similarity_feature, rs_similarity)


# use w2v feature
path_w2v_feature = '../data/w2v_feature'
if check_score_exist(path_w2v_feature+'_max'):
    rs_w2v_min = load_feature_score(path_w2v_feature+'_min')
    rs_w2v_max = load_feature_score(path_w2v_feature+'_max')
    rs_w2v_avg = load_feature_score(path_w2v_feature+'_avg')
else:
    rs_w2v_min, rs_w2v_max, rs_w2v_avg = w2v_feature(texts, ans)
    dump_feature_score(path_w2v_feature+'_min', rs_w2v_min)
    dump_feature_score(path_w2v_feature+'_max', rs_w2v_max)
    dump_feature_score(path_w2v_feature+'_avg', rs_w2v_avg)

'''
# use google distance feature
# not useful at all
path_google_dis_feature = '../data/google_dis_feature'
if check_score_exist(path_google_dis_feature+'_min'):
    rs_google_dis_min = load_feature_score(path_google_dis_feature+'_min')
    rs_google_dis_max = load_feature_score(path_google_dis_feature+'_max')
    rs_google_dis_avg = load_feature_score(path_google_dis_feature+'_avg')
else:
    print "google"
    rs_google_dis_min, rs_google_dis_max, rs_google_dis_avg = google_dis_feature(texts, ans)
    dump_feature_score(path_google_dis_feature+'_min', rs_google_dis_min)
    dump_feature_score(path_google_dis_feature+'_max', rs_google_dis_max)
    dump_feature_score(path_google_dis_feature+'_avg', rs_google_dis_avg)
'''



# main
# make X
X = combine_f(rs_retrieval, rs_similarity, rs_w2v_min, rs_w2v_max)
X = combine_f(rs_retrieval, rs_similarity)
# make y
y = correct_label_alpha2num()


training_size = 9.0
num_samples = y.shape[0]
train = range(int(num_samples*training_size))
test = range(int(num_samples*training_size), num_samples)

X_train, y_train = X[train], y[train]

num_samples = y.shape[0]
X_test, y_test = X[test], y[test]


#weight = fit_perceptron(X_train, y_train, epoch=100)
weight = ([[1639031.09625254], [3164.16903221]], 40142.50000010997)
print 'weight from perceptron: {}'.format(weight)
pre_y = pre_perceptron(weight, X_test)
print len(pre_y)
print pre_y
y_hat = correct_label_num2alpha(pre_y)
y_t = correct_label_num2alpha(y_test)

p = get_performance(y_hat, y_t)

print y_hat
print y_t


from collections import Counter
print Counter(y_hat)
print Counter(y_t)
print p

