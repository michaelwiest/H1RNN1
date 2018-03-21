from fasta_sampler_v2 import *
from RNN_v3 import *
import csv

batch_size = 20
# List of lists of kernel sizes. Kernels in same list are sequential
# Kernels in separate lists happen in parallel.
kernel_sizes = []
# Filter sizes associated with kernels above. Will throw an error if they
# dont' match
num_filters = []

dilation = [0, 1, 0] # Deprecated
lstm_hidden_units = 100
# num_filters = 64
samples_per_epoch = 100000
num_epochs = 5
learning_rate = 0.005
seq_length = 200
seq_length_incr_perc = 0.1

# Build the data handler object.
fs = FastaSamplerV2('data/HA_n_2010_2018.fa', 'data/HA_s_2010_2018.fa')
# Assign the validation years.
fs.set_validation_years([2013, 2014, 2015, 2016, 2017])
vocab = fs.vocabulary


use_gpu = torch.cuda.is_available()


rnn = RNN(1, num_filters, len(vocab.keys()), kernel_sizes, dilation, lstm_hidden_units,
          use_gpu, batch_size)

model_name = 'model.pt'
log_name = 'log.csv'
train_loss, val_loss = rnn.train(fs, batch_size,
                                 num_epochs,
                                 learning_rate,
                                 samples_per_epoch=samples_per_epoch,
                                 save_params=(model_name, log_name),
                                 slice_len=None,
                                 slice_incr_perc=None
                                 )


torch.load('model.pt', map_location=lambda storage, loc: storage)

# rnn.load_state_dict(torch.load('model.pt'))
# rnn.cuda(device_id=0)

ex = fs.generate_N_sample_per_year(1, 2012, full=False, to_num=False)[0]
dream = rnn.daydream1(rnn, ex, 5, fs, predict_len=566)
print ('ex:')
print (ex)
print(dream)
print(len(dream))
