#! /usr/bin/env python
# _*_coding:utf-8_*_
# project: SemEval2019
# Author: zcj
# @Time: 2019/1/21 12:49

import os
import sys
import logging
import pickle
import numpy as np
import pandas as pd

from keras.models import Model
from keras.layers import Dense, Dropout, Embedding, LSTM, GRU, Bidirectional, Input, RepeatVector, Permute, \
    TimeDistributed
from keras.preprocessing import sequence
from sklearn.model_selection import StratifiedKFold, KFold #分层k折交叉验证
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.utils import np_utils
from keras.models import load_model
from metrics import f1

# maxlen = 56
batch_size = 256
nb_epoch = 40
# nb_epoch = 1

hidden_dim = 120

kernel_size = 3
nb_filter = 60

train = pd.read_csv("./task_b_train/train1.tsv", header=0, sep="\t", quoting=3, )
# test = pd.read_csv("./test_data/testset-taska.tsv", header=0, sep="\t", quoting=3, )


# train["subtask_b"] = train["subtask_b"].replace({"TIN": 0, "UNT": 1})



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
    pickle_file = os.path.join('pickle', 'SemEval_train_val_test_TASK_B_TRAIL2.pickle3')

    revs, W, word_idx_map, vocab, maxlen = pickle.load(open(pickle_file, 'rb'))
    logging.info('data loaded!')

    X_train, X_test, X_dev, y_train, y_dev = make_idx_data(revs, word_idx_map, maxlen = maxlen)

    # print("X_train", X_train.shape)  # (3546, 102)
    # print("y_train", y_train.shape)  # (3546, 2)
    # print("X_dev", X_dev.shape)  # (854, 102)
    # print(" y_dev", y_dev.shape)  # (854, 2)

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
    # hidden = Bidirectional(LSTM(hidden_dim//2, recurrent_dropout=0.25)) (embedded)

    # bi-directional GRU
    hidden = Bidirectional(GRU(hidden_dim // 2, recurrent_dropout=0.25))(embedded)

    output = Dense(2, activation='softmax')(hidden)
    model = Model(inputs=sequence, outputs=output)
    class_weight = {0:1,1:7}

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc',f1])

    train_num, test_num = X_train.shape[0], X_dev.shape[0]
    num1 = y_train.shape[1]
    # print(y_train.shape[1])     2
    # print(x_train.shape[0])     #10556
    # print(x_test.shape[0])      #2684

    second_level_train_set = np.zeros((train_num, num1))  # (10556,)
    # print(second_level_train_set.shape)      # (10556,)
    second_level_test_set = np.zeros((test_num, num1))  # (2684,)
    # print(second_level_test_set.shape)       # (2684,)
    # test_nfolds_sets = np.zeros((test_num, n_folds))     #(2684,5)
    test_nfolds_sets = []

    # print(np.zeros((test_num, n_folds)).shape)
    # print(test_nfolds_sets[:].shape)

    kf = KFold(n_splits=5)

    for i, (train_index, test_index) in enumerate(kf.split(X_train)):
        # print(i)     i 从0开始
        # print(train_index.shape)                #(8444)         train_index + test_index = x_train.shape[0]
        # print(test_index.shape)               #  (2112)

        x_tra, y_tra = X_train[train_index], y_train[train_index]
        # print(x_tra.shape)             #  (8444,104)
        # print(y_tra.shape)             #   （8444,2）
        x_tst, y_tst = X_train[test_index], y_train[test_index]
        # print(x_tst.shape)             #（2112,104）
        # print(y_tst.shape)             #  （2112,2）
        # print(x_tst.shape)                   #  (2112, 104)
        # print(x_tst.shape[0])                #2112
        # print(x_tst.shape[1])                # 104
        # print(x_tst[0].shape)               #  (104,)
        # print(x_tst[0])
        # print(x_tst[1])
        # print("x_tst:",x_tst)

        checkpointer = ModelCheckpoint(filepath="weights.hdf5", monitor='val_acc', verbose=1, save_best_only=True)
        early_stopping = EarlyStopping(monitor='val_acc', patience=12, verbose=1)

        model.fit(x_tra, y_tra, validation_data=[x_tst, y_tst], batch_size=batch_size, epochs=nb_epoch, verbose=2,
                  class_weight=class_weight, callbacks=[checkpointer, early_stopping])
        # clf.fit(x_tra, y_tra)
        # x_tst = x_tst.reshape((x_tst.shape[0],))



        second_level_train_set[test_index] = model.predict(x_tst, batch_size=batch_size)  # (2112,2) could not be broadcast to indexing result of shape (2112,)
        # second_level_train_set[test_index].shape                (2112,)
        # print(test_nfolds_sets[:, i].shape)                   # (2684,)
        # test_nfolds_sets[:,i] = clf.predict(x_test)              #  from shape (2684,2) into shape (2684)
        # second_level_test_set[:] = clf.predict(x_test, batch_size = batch_size)
        test_nfolds_sets.append(model.predict(X_dev))
    for item in test_nfolds_sets:
        second_level_test_set += item

    second_level_test_set = second_level_test_set / 5



    # model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2, class_weight = class_weight,callbacks=[checkpointer,early_stopping])
    # print(X_train.shape)     (11937,104)
    # print(y_train.shape)     (11937, 2)
    # print(X_dev.shape)       (1303, 104)
    # print(y_dev.shape)        (1303,2 )

    # model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2,)
    # model = load_model('weights.hdf5')

    # y_pred = model.predict(X_dev, batch_size=batch_size)
    y_pred = second_level_test_set
    # print(y_pred.shape)         #(1303,2)
    # print(y_pred)
    y_pred = np.argmax(y_pred, axis=1)
    # print(y_pred)    #  [0 0 1 ... 0 1 1]
    y_dev = np.argmax(y_dev, axis=1)


    # y_pred = model.predict(X_test, batch_size = batch_size)
    # y_pred = np.argmax(y_pred, axis=1)
    #
    # result_output = pd.DataFrame(data={"id":test["id"], "label":y_pred})

    # Use pandas to write the comma-separated output file
    # result_output.to_csv("./result/bi-lstm.csv", index=False, quoting=3, header = 0 )
    # result_output.to_csv("./result/bi-lstm.csv", index=False, quoting=3)

    # result_output.to_csv("./result/bi-lstm1.csv", index=False, quoting=3)



from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

print(precision_score(y_dev, y_pred, average='macro'))
print(recall_score(y_dev, y_pred, average='macro'))
print(accuracy_score(y_dev, y_pred))
print(f1_score(y_dev, y_pred, average='macro'))
