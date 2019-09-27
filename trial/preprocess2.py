#! /usr/bin/env python
# _*_coding:utf-8_*_
# project: SemEval2019
# Author: zcj
# @Time: 2018/12/23 12:27

import os
import sys
import logging
import re
import nltk
import gensim
import pickle
import io

import numpy as np
import pandas as pd
from stanford_tokenizer_config import *
from collections import defaultdict

train = pd.read_csv("./train_data/train_subtask_a", header=0, sep="\t", quoting=3, )

train["subtask_a"] = train["subtask_a"].replace({"NOT": 0, "OFF": 1})


def review_to_wordlist(review):
    #  Remove non-letters
    review_text = re.sub("[^a-zA-Z]", " ", review)

    #  Convert words to lower case and split them
    words = review_text.lower()

    words = nltk.word_tokenize(words)
    # words = nltk.TweetTokenizer().tokenize(words)
    # words = stanford_tokenizer(words)

    return (words)


def build_data_train_test(data_train, data_test, train_ratio=0.8):
    """
    Loads data and process data into index
    """
    revs = []
    vocab = defaultdict(float)

    # Pre-process train data set
    for i in range(len(data_train)):
        rev = data_train[i]
        y = train["subtask_a"][i]
        # print("y:", y)
        orig_rev = ' '.join(rev).lower()
        # print(type(orig_rev))  # str
        words = set(orig_rev.split())
        for word in words:
            vocab[word] += 1
        datum = {'y': y,
                 'text': orig_rev,
                 'num_words': len(orig_rev.split()),
                 'split': int(np.random.rand() < train_ratio)}
        revs.append(datum)

    for i in range(len(data_test)):
        rev = data_test[i]
        orig_rev = ' '.join(rev).lower()

        words = set(orig_rev.split())
        for word in words:
            vocab[word] += 1
        datum = {'y': -1,
                 'text': orig_rev,
                 'num_words': len(orig_rev.split()),
                 'split': -1}
        revs.append(datum)

    return revs, vocab


def load_bin_vec(model, vocab):
    word_vecs = {}
    unk_words = 0

    for word in vocab.keys():
        try:
            word_vec = model[word]
            word_vecs[word] = word_vec
        except:
            unk_words = unk_words + 1

    logging.info('unk words: %d' % (unk_words))
    return word_vecs


def get_W(word_vecs, k = 300):
    vocab_size = len(word_vecs)
    word_idx_map = dict()

    W = np.zeros(shape=(vocab_size + 2, k), dtype=np.float32)
    W[0] = np.zeros((k,))
    W[1] = np.random.uniform(-0.25, 0.25, k)

    i = 2
    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
        i = i + 1
    return W, word_idx_map


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ''.join(sys.argv))

    clean_train_reviews = []
    for review in train['tweet']:
        clean_train_reviews.append(review_to_wordlist(review))

    clean_test_reviews = []
    # for review in test['tweet']:
    #     clean_test_reviews.append(review_to_wordlist(review))

    revs, vocab = build_data_train_test(clean_train_reviews, clean_test_reviews)
    max_l = np.max(pd.DataFrame(revs)['num_words'])
    logging.info('data loaded!')
    logging.info('number of sentences: ' + str(len(revs)))
    logging.info('vocab size: ' + str(len(vocab)))
    logging.info('max sentence length: ' + str(max_l))

    # word2vec GoogleNews
    # model_file = os.path.join('vector', 'GoogleNews-vectors-negative300.bin')
    # model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)

    # Glove Common Crawl
    # model_file = os.path.join('vector', 'glove.840B.300d.txt')
    # model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=False)

    embeddingsIndex = {}

    with io.open(os.path.join('vector', 'glove.twitter.27B.200d.txt'), encoding="utf8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            embeddingVector = np.asarray(values[1:],dtype='float32' )
            embeddingsIndex[word] = embeddingVector

    w2v = load_bin_vec(embeddingsIndex, vocab)
    # w2v = load_bin_vec(model, vocab)
    logging.info('word embeddings loaded!')
    logging.info('num words in embeddings: ' + str(len(w2v)))

    W, word_idx_map = get_W(w2v, k = 200)
    logging.info('extracted index from embeddings! ')

    # pickle_file = os.path.join('pickle', 'vader_movie_reviews_glove.pickle3')
    pickle_file = os.path.join('pickle', 'imdb_train_val_test_nltk_word_tokenize.pickle3')
    pickle.dump([revs, W, word_idx_map, vocab, max_l], open(pickle_file, 'wb'))
    logging.info('dataset created!')