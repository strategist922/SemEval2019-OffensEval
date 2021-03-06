#! /usr/bin/env python
# _*_coding:utf-8_*_
# project: SemEval2019
# Author: zcj
# @Time: 2019/1/17 1:20

import os
import sys
import logging
import pandas as pd
import numpy as np
import pickle

from util import save_result
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.layers import Dense, Input, SpatialDropout1D, CuDNNGRU, Dropout, MaxPooling2D, Flatten, LSTM, MaxPooling1D, Embedding, Bidirectional, GRU
from keras.models import Model
from keras.models import load_model
from keras.wrappers.scikit_learn import KerasClassifier
from Attention_layer import AttentionM
from capsule_net import Capsule
from vote_classifier import VotingClassifier
from metrics import f1
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

train = pd.read_csv("./train_data/train_subtask_a.tsv", header = 0, sep = "\t", quoting = 3, )
test = pd.read_csv("./test_data/testset-taska.tsv", header = 0, sep = "\t", quoting = 3, )


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


def make_idx_data(revs, word_idx_map, maxlen=60):
    """
    Transforms sentences into a 2-d matrix.
    """
    X_train, X_test, X_dev, y_train, y_dev,= [], [], [], [], []
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
    y_train = np_utils.to_categorical(np.array(y_train))
    y_dev = np_utils.to_categorical(np.array(y_dev))

    return [X_train, X_test, X_dev, y_train, y_dev,]


def bi_lstm_model(batch_size, nb_epoch, hidden_dim, num):
    sequence = Input(shape=(maxlen,), dtype='int32')

    embedded = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, mask_zero=True,
                         weights=[W], trainable=False)(sequence)

    embedded = Dropout(0.25)(embedded)

    # bi-directional LSTM
    hidden = Bidirectional(LSTM(hidden_dim // 2, recurrent_dropout=0.25))(embedded)

    output = Dense(2, activation='softmax')(hidden)
    model = Model(inputs=sequence, outputs=output)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', f1])


    model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2,)

    model.save("weights_bi_lstm" + num + ".hdf5")

    y_pred = model.predict(X_test, batch_size=batch_size)

    return y_pred

def bi_gru_model(batch_size, nb_epoch, hidden_dim, num):
    sequence = Input(shape=(maxlen,), dtype='int32')

    embedded = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, mask_zero=True,
                         weights=[W], trainable=False)(sequence)

    embedded = Dropout(0.25)(embedded)

    # bi-directional GRU
    hidden = Bidirectional(GRU(hidden_dim // 2, recurrent_dropout=0.25))(embedded)

    output = Dense(2, activation='softmax')(hidden)
    model = Model(inputs=sequence, outputs=output)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', f1])

    model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2,)

    model.save("weights_bi_gru" + num + ".hdf5")

    y_pred = model.predict(X_test, batch_size=batch_size)

    return y_pred


def attention_lstm_model(batch_size, nb_epoch, hidden_dim, num):
    sequence = Input(shape=(maxlen,), dtype='int32')

    embedded = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, mask_zero=True,
                         weights=[W], trainable=False)(sequence)

    embedded = Dropout(0.25)(embedded)

    # bi-lstm
    enc = Bidirectional(LSTM(hidden_dim // 2, recurrent_dropout=0.25, return_sequences=True))(embedded)

    att = AttentionM()(enc)

    fc1_dropout = Dropout(0.25)(att)
    fc1 = Dense(50, activation="relu")(fc1_dropout)
    fc2_dropout = Dropout(0.25)(fc1)

    output = Dense(2, activation='softmax')(fc2_dropout)
    model = Model(inputs=sequence, outputs=output)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', f1])

    model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2,)

    model.save("weights_attention_lstm" + num  + ".hdf5")
    y_pred = model.predict(X_test, batch_size=batch_size)

    return y_pred



def capsulnet_model(batch_size, nb_epoch, hidden_dim, num):
    Routings = 15
    Num_capsule = 30
    Dim_capsule = 60

    sequence_input = Input(shape=(maxlen,), dtype='int32')
    embedded_sequences = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, weights=[W],
                                   trainable=False)(sequence_input)
    embedded_sequences = SpatialDropout1D(0.1)(embedded_sequences)
    x = Bidirectional(CuDNNGRU(64, return_sequences=True))(embedded_sequences)
    x = Bidirectional(CuDNNGRU(64, return_sequences=True))(x)
    capsule = Capsule(num_capsule=Num_capsule, dim_capsule=Dim_capsule, routings=Routings, share_weights=True)(x)
    # output_capsule = Lambda(lambda x: K.sqrt(K.sum(K.square(x), 2)))(capsule)
    capsule = Flatten()(capsule)
    capsule = Dropout(0.4)(capsule)
    output = Dense(2, activation='softmax')(capsule)
    model = Model(inputs=[sequence_input], outputs=output)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', f1])

    model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2,
              shuffle=False,)
    model.save("weights_capsulnet" + num + ".hdf5")
    y_pred = model.predict(X_test, batch_size=batch_size)

    return y_pred


def stacked_lstm_model(batch_size, nb_epoch, hidden_dim, num):
    sequence = Input(shape=(maxlen,), dtype='int32')

    embedded = Embedding(input_dim=max_features, output_dim=num_features, input_length=maxlen, mask_zero=True,
                         weights=[W], trainable=False)(sequence)

    embedded = Dropout(0.25)(embedded)

    # bi-directional LSTM
    hidden = Bidirectional(LSTM(hidden_dim // 2, recurrent_dropout=0.25, return_sequences=True))(embedded)
    hidden = Bidirectional(LSTM(hidden_dim // 2, recurrent_dropout=0.25))(hidden)


    output = Dense(2, activation='softmax')(hidden)
    model = Model(inputs=sequence, outputs=output)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', f1])

    model.fit(X_train, y_train, validation_data=[X_dev, y_dev], batch_size=batch_size, epochs=nb_epoch, verbose=2,)
    model.save("weights_stacked_lstm" + num + ".hdf5")

    y_pred = model.predict(X_test, batch_size=batch_size)

    return y_pred

if __name__ == '__main__':

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info(r"running %s" % ''.join(sys.argv))

    logging.info('loading data...')

    pickle_file = os.path.join('pickle', 'SemEval_train_val_test_teminal.pickle3')

    revs, W, word_idx_map, vocab, maxlen = pickle.load(open(pickle_file, 'rb'))
    logging.info('data loaded!')

    X_train, X_test, X_dev, y_train, y_dev = make_idx_data(revs, word_idx_map, maxlen=maxlen)

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


    bi_lstm_pre1 = bi_lstm_model(256, 20, 120, '1')
    bi_lstm_pre2 = bi_lstm_model(256, 20, 120, '2')
    bi_lstm_pre3 = bi_lstm_model(256, 20, 120, '3')
    bi_lstm_pre4 = bi_lstm_model(256, 20, 120, '4')
    bi_lstm_pre5 = bi_lstm_model(256, 20, 120, '5')
    bi_lstm_pre = (bi_lstm_pre1 + bi_lstm_pre2 + bi_lstm_pre3 + bi_lstm_pre4 + bi_lstm_pre5) / 5

    bi_gru_pre1 = bi_gru_model(100, 18, 120, '1')
    bi_gru_pre2 = bi_gru_model(100, 18, 120, '2')
    bi_gru_pre3 = bi_gru_model(100, 18, 120, '3')
    bi_gru_pre4 = bi_gru_model(100, 18, 120, '4')
    bi_gru_pre5 = bi_gru_model(100, 18, 120, '5')
    bi_gru_pre = (bi_gru_pre1 + bi_gru_pre2 + bi_gru_pre3 + bi_gru_pre4 + bi_gru_pre5) / 5

    attention_lstm_pre1 = attention_lstm_model(256, 16, 120, '1')
    attention_lstm_pre2 = attention_lstm_model(256, 16, 120, '2')
    attention_lstm_pre3 = attention_lstm_model(256, 16, 120, '3')
    attention_lstm_pre4 = attention_lstm_model(256, 16, 120, '4')
    attention_lstm_pre5 = attention_lstm_model(256, 16, 120, '5')
    attention_lstm_pre = (attention_lstm_pre1 + attention_lstm_pre2 + attention_lstm_pre3 + attention_lstm_pre4 + attention_lstm_pre5) / 5


    capsulnet_pre1 = capsulnet_model(100, 20, 120, "1")
    capsulnet_pre2 = capsulnet_model(100, 20, 120, "2")
    capsulnet_pre3 = capsulnet_model(100, 20, 120, "3")
    capsulnet_pre4 = capsulnet_model(100, 20, 120, "4")
    capsulnet_pre5 = capsulnet_model(100, 20, 120, "5")
    capsulnet_pre = (capsulnet_pre1 + capsulnet_pre2 + capsulnet_pre3 + capsulnet_pre4 + capsulnet_pre5) / 5

    stacked_pre1 = stacked_lstm_model(128, 24, 120, '1')
    stacked_pre2 = stacked_lstm_model(128, 24, 120, '2')
    stacked_pre3 = stacked_lstm_model(128, 24, 120, '3')
    stacked_pre4 = stacked_lstm_model(128, 24, 120, '4')
    stacked_pre5 = stacked_lstm_model(128, 24, 120, '5')
    stacked_pre = (stacked_pre1 + stacked_pre2 + stacked_pre3 + stacked_pre4 + stacked_pre5) / 5

    y_pred = (bi_lstm_pre + bi_gru_pre + attention_lstm_pre + capsulnet_pre + stacked_pre)
    y_pred = np.argmax(y_pred, axis=1)



    result_output = pd.DataFrame(data={"id": test["id"], "label": y_pred}, )

    result_output.to_csv("./result/task_a_submission_voting.csv", index=False, quoting=3, )




