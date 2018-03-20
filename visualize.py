from fasta_sampler_v2 import *
from RNN_v2 import *
import numpy as np
from Bio import SeqIO
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from helper_v2 import get_idx
from collections import Counter
import scipy
from helper import *

class Visualize():
    def __init__(self, year, fs, rnn):
        self.year = year
        self.vocab = fs.vocabulary
        self.fs = fs
        self.rnn = rnn

    def distance_heatmap(self):
        self.fs.get_data()
        predicted = self.rnn.batch_dream(len(self.fs.data_mat[str(self.year+1)+'n']), '$M', self.year, 5, self.fs, predict_len=566)
        num_mat = self.fs.num_mat

        num_pred = [[self.vocab[c] for c in sequence] for sequence in self.predicted]
        dist_mat = scipy.spatial.distance.cdist(num_mat[str(self.year)+self.hemisphere], num_pred, 'hamming')
        plt.imshow(dist_mat, cmap='PiYG', interpolation='nearest')
        plt.colorbar()
        plt.style.use('fivethirtyeight')
        plt.xlabel(str(self.year)+self.hemisphere)
        plt.ylabel(str(year+1)+'n')
        plt.title('Distances between proteins')
        return dist_mat

model = torch.load('random_fasta.pt', map_location=lambda storage, loc: storage)

batch_size = 30
kernel_sizes = [3, 5]
num_filters = [16, 64]
samples_per_epoch = 50000
num_epochs = 15
learning_rate = 0.003
seq_len = 100
slice_incr_perc = 0.1

use_gpu = torch.cuda.is_available()
fs = FastaSamplerV2('data/HA_n_2010_2018.fa', 'data/HA_s_2010_2018.fa')
fs.set_validation_years([2016, 2017])

primer = [fs.vocabulary[c] for c in list('$M')]

rnn = RNN(1,
          num_filters,
          len(fs.vocabulary.keys()),
          kernel_sizes,
          use_gpu,
          batch_size
          )
# prevs, m0, t = fs.generate_N_random_samples_and_targets(1)
#(self, N, primer, year, T, fasta_sampler,predict_len)
predicted = fs.data_mat['2016n']
vis = Visualize(2017,fs)
dist_mat = vis.distance_heatmap()
plt.show()
# plt.imshow(dist_mat, cmap='hot', interpolation='nearest')
# plt.show()
