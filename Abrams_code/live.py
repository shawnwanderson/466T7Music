'''
Copyright (c) 2013-2015, Gregory Burlet, Abram Hindle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


from __future__ import division
from theano import config
import theano
config.experimental.unpickle_gpu_on_cpu = True
#config.force_device = True
import os
import argparse
import numpy as np
import pickle
import time
import logging
from glob import glob
from random import shuffle
from sextract import StreamFeatureExtractor
from dbn import DBN
import theano.tensor as T 
import liblo

# command line arguments
parser = argparse.ArgumentParser(description='Live Pitches!')
# parser.add_argument('ain', help='Path of (.wav) audio files for training/validation/testing')
# parser.add_argument('lin', help='Path of (.midi) label files for training/validation/testing')
#parser.add_argument('tmp', help='Path of directory to write intermediary or data save files',default="./tmp/")
args = parser.parse_args()

# experiment logger
logging.basicConfig(filename=os.path.join("tmp/live.log"), level=logging.INFO, format='')

# set RNG seed such that training/testing split is the same across experiment runs
np.random.seed(2)

#####################################################################################
#                              Experiment Parameters                                #
#####################################################################################
fs = 22050                                              # sampling rate
dataset_partition = [0.8, 0.2]                          # 80% training, 20% testing
num_folds = 5                                           # for k-fold cv
w = 1024                                                # window size (samples)
h = 768                                                 # hop size (samples)
hidden_layers = [400, 300]                              # hidden layer sizes
featuredef = {"type": "STFT"}                           # feature type

cont_train = False                                      # train for ft_epoch more iterations
pt_epoch = 400                                          # pretrain epochs
pt_lr = 0.05                                            # pretrain learning rate 
pt_k = 1                                                # pretrain k-step CD
pt_thresh = 1e-20                                       # pretrain convergence thresh
pt_batch_size = 1000                                    # pretrain batch size
ft_epoch = 30000                                        # finetune epochs
ft_lr = 0.05                                            # finetune learning rate
ft_k = 1                                                # finetune k-step CD
ft_thresh = 1e-20                                       # finetune convergence thresh
ft_batch_size = 1000                                    # finetune batch size

onset_thresh = 0.5                                      # 250ms grace time for note onsets
offset_range = 0.75                                      # 20% duration grace time for offsets
#####################################################################################

#dbn = pickle.load(file("ex7_dbn_w1024_h768_fs22050_STFT_[400_300].pkl",'rb'))
dbn = pickle.load(file("cpu-trained.pkl",'rb'))
from time import sleep
fe = StreamFeatureExtractor(w, h, featuredef, int(44100/fs), True)
target = liblo.Address(57120)

midioffset = 21

while True:
    sample = fe.extract_features()
    # sample = theano.shared(np.zeros([1, 513], dtype=np.float32), borrow=False)
    if not sample == None:
        pred = dbn.make_predictions(sample)
        print pred[1]
        midis = pred[0][0].tolist()
        liblo.send(target, "/livetracker/pitch", *pred[0][0].tolist())
        liblo.send(target, "/livetracker/voices", pred[1][0])
        liblo.send(target, "/livetracker/raw", *pred[2][0].tolist())
        for i in range(0,len(midis)):
            if midis[i] > 0:
                liblo.send(target, "/livetracker/midi", midioffset + i)
    #sleep(0.01)

