#! /usr/bin/env python
# _*_coding:utf-8_*_
# project: SemEval2019
# Author: zcj
# @Time: 2019/1/26 16:52

import os
import sys
import logging
import pickle
import numpy as np
import pandas as pd

from keras.models import Model
from keras.layers import Dense, Dropout, Embedding, LSTM, GRU, Bidirectional, Input, RepeatVector, Permute, \
    TimeDistributed
from sklearn.model_selection import StratifiedKFold, KFold #分层k折交叉验证
from keras.preprocessing import sequence

from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.utils import np_utils
from keras.models import load_model
from metrics import f1

# maxlen = 56
batch_size = 100
nb_epoch = 35
# nb_epoch = 1

hidden_dim = 120

kernel_size = 3
nb_filter = 60

train = pd.read_csv("./task_c_train/train.tsv", header=0, sep="\t", quoting=3, )
# test = pd.read_csv("./test_data/testset-taskb.tsv", header=0, sep="\t", quoting=3, )

train["subtask_c"] = train["subtask_c"].replace({"IND": 0, "GRP": 1, "OTH": 2})



def get_idx_from_sent(sent, word_idx_map):
    """
    Transforms sentence into a list of indices. Pad with zeroes.
    """
    x = []
    words = sent.split()
    for word in words:
        if word in word_idx_map:
            x.append(word_idx_map[word])
        else:
            x.append(1)

    return x


def make_idx_data(revs, word_idx_map, maxlen = 150):
    """
    Transforms sentences into a 2-d matrix.
    :读取rev中的text字段，传入get_idx_from_sent()方法，将句子转换成一个list，list里面的元素是这句话每个词的索引.
    这个list形如(filter padding) - (word indices) - (Max padding) - (filter padding)，长度为max_l+2×(filter_h-1)，
    每句句子虽然本身长度不同，经过这步都转换成相同长度的list。然后，按照cv索引，分割训练集和测试集

    """
    X_train, X_test, X_dev, y_train, y_dev = [], [], [], [], []
    for rev in revs:
        sent = get_idx_from_sent(rev['text'], word_idx_map)
        y = rev['y']

        if rev['split'] == 1:
            X_train.append(sent)
            y_train.append(y)
        elif rev['split'] == 0:
            X_dev.append(sent)
            y_dev.append(y)
        elif rev['split'] == -1:
            X_test.append(sent)

    X_train = sequence.pad_sequences(np.array(X_train), maxlen=maxlen)
    X_dev = sequence.pad_sequences(np.array(X_dev), maxlen=maxlen)
    X_test = sequence.pad_sequences(np.array(X_test), maxlen=maxlen)
    # X_valid = sequence.pad_sequences(np.array(X_valid), maxlen=maxlen)
    y_train = np_utils.to_categorical(np.array(y_train))
    y_dev = np_utils.to_categorical(np.array(y_dev))
    # y_valid = np.array(y_valid)

    return [X_train, X_test, X_dev, y_train, y_dev]


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info(r"running %s" % ''.join(sys.argv))

    logging.info('loading data...')
    # pickle_file = os.path.join('pickle', 'vader_movie_reviews_glove.pickle3')
    # pickle_file = sys.argv[1]
    pickle_file = os.path.join('pickle', 'SemEval_train_val_test_TASK_C1.pickle3')

    revs, W, word_idx_map, vocab, maxlen = pickle.load(open(pickle_file, 'rb'))
    logging.info('data loaded!')

    X_train, X_test, X_dev, y_train, y_dev = make_idx_data(revs, word_idx_map, maxlen = maxlen)

    n_train_sample = X_train.shape[0]
    logging.info("n_train_sample [n_train_sample]: %d" % n_train_sample)

    n_test_sample = X_test.shape[0]
    logging.info("n_test_sample [n_train_sample]: %d" % n_test_sample)

    len_sentence = X_train.shape[1]  # 200
    logging.info("len_sentence [len_sentence]: %d" % len_sentence)

    max_features = W.shape[0]
    logging.info("num of word vector [max_features]: %d" % max_features)

    num_features = W.shape[1]  # 400
    logging.info("dimension of word vector [num_features]: %d" % num_features)

    # Keras Model
    # this is the placeholder tensor for the input sequence
    sequence = Input(shape=(maxlen,), dtype='int32')

    embedded = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, mask_zero=True,
                         weights=[W], trainable=False)(sequence)
    # embedded = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, weights=[W], trainable=False) (sequence)
    embedded = Dropout(0.25)(embedded)

    # bi-directional LSTM
    hidden = Bidirectional(LSTM(hidden_dim//2, recurrent_dropout=0.25)) (embedded)

    # bi-directional GRU
    # hidden = Bidirectional(GRU(hidden_dim // 2, recurrent_dropout=0.25))(embedded)

    output = Dense(3, activation='softmax')(hidden)
    model = Model(inputs=sequence, outputs=output)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc',f1])

    # checkpointer = ModelCheckpoint(filepath="weights.hdf5", monitor='val_acc', verbose=1, save_best_only=True)
    # early_stopping = EarlyStopping(monitor='val_f1', patience = 15, verbose=1)
    class_weight = {0:1, 1:2, 2:6}
    train_num, test_num = X_train.shape[0], X_dev.shape[0]
    num1 = y_train.shape[1]


    second_level_train_set = np.zeros((train_num, num1))  # (10556,)

    second_level_test_set = np.zeros((test_num, num1))  # (2684,)

    test_nfolds_sets = []



    kf = KFold(n_splits=5)

    for i, (train_index, test_index) in enumerate(kf.split(X_train)):


        x_tra, y_tra = X_train[train_index], y_train[train_index]

        x_tst, y_tst = X_train[test_index], y_train[test_index]


        checkpointer = ModelCheckpoint(filepath="weights.hdf5", monitor='val_acc', verbose=1, save_best_only=True)
        early_stopping = EarlyStopping(monitor='val_acc', patience=14, verbose=1)

        model.fit(x_tra, y_tra, validation_data=[x_tst, y_tst], batch_size=batch_size, epochs=nb_epoch, verbose=2,
                  class_weight=class_weight, callbacks=[checkpointer, early_stopping])


        second_level_train_set[test_index] = model.predict(x_tst,
                                                           batch_size=batch_size)  # (2112,2) could not be broadcast to indexing result of shape (2112,)

        test_nfolds_sets.append(model.predict(X_dev))
    for item in test_nfolds_sets:
        second_level_test_set += item

    second_level_test_set = second_level_test_set / 5


    y_pred = second_level_test_set
    y_pred = np.argmax(y_pred, axis=1)
    y_dev = np.argmax(y_dev, axis=1)

from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

print(precision_score(y_dev, y_pred, average='macro'))
print(recall_score(y_dev, y_pred, average='macro'))
print(accuracy_score(y_dev, y_pred))
print(f1_score(y_dev, y_pred, average='macro'))
