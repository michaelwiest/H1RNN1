from fasta_sampler import *
from models.RNN import *
from helper import *
import csv
import numpy as np

batch_size = 30
# List of lists of kernel sizes. Kernels in same list are sequential
# Kernels in separate lists happen in parallel.
kernel_sizes = [3, 5]
# Filter sizes associated with kernels above. Will throw an error if they
# dont' match
num_filters = [16, 64]
samples_per_epoch = 50000
num_epochs = 15
learning_rate = 0.003
seq_len = 100
slice_incr_perc = 0.1

# Build the data handler object.
fs = FastaSampler('data/HA_n_2010_2018.fa', 'data/HA_s_2010_2018.fa')
# Assign the validation years.
fs.set_validation_years([2016, 2017, 2015, 2014, 2013])
vocab = fs.vocabulary


use_gpu = torch.cuda.is_available()

rnn = RNN(1,
          num_filters,
          len(vocab.keys()),
          kernel_sizes,
          use_gpu,
          batch_size
          )

model_name = 'model.pt'
log_name = 'log.csv'
train_loss, val_loss = rnn.do_training(fs, batch_size,
                                       num_epochs,
                                       learning_rate,
                                       samples_per_epoch=samples_per_epoch,
                                       save_params=(model_name, log_name),
                                       slice_len=seq_len,
                                       slice_incr_perc=slice_incr_perc
                                       )
print(rnn.batch_dream(5, '$M', 2012, 1, fs, 566))
