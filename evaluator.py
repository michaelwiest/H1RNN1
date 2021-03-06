from fasta_sampler_v2 import *
from RNN_v2 import *
import scipy
'''
Usage is:
E = Evaluator(fs, model)
dist, pred, actual = E.gen_and_compare_year(10, '$MK', 2012, 10)
'''

class Evaluator(object):
    def __init__(self, fasta_sampler, model):
        self.fs = fasta_sampler
        self.model = model

    def get_dist_matrix(self, seqs_a, seqs_b):
        '''
        Returns a numpy array of the distance between sequences a and b.
        You should supply a 2d array of characters.
        Where each row is a sequence ie,['M', 'K', ...]
        '''
        if len(seqs_a.shape) == 1:
            seqs_a = np.array([seqs_a]).T
        if len(seqs_b.shape) == 1:
            seqs_b = np.array([seqs_b]).T
        seqs_a = np.vectorize(self.fs.vocabulary.get)(seqs_a)
        seqs_b = np.vectorize(self.fs.vocabulary.get)(seqs_b)
        return scipy.spatial.distance.cdist(seqs_a, seqs_b, metric='hamming')


    def gen_and_compare_year(self, num_samples, primer, year, temp):
        '''
        Dreams up a batch of guesses from the model. And compares them to the
        Following year's data (the year for which it would be predicting).
        '''
        dollar = False
        if primer.startswith('$'):
            dollar = True

        predict_len = self.fs.specified_len - len(primer)
        if dollar:
            predict_len += 1
        predictions = self.model.batch_dream(num_samples, primer, year, temp,
                                             self.fs, predict_len, split=True)
        if dollar:
            predictions = predictions[:, 1:]
        df = self.fs.to_dataframe()
        df = df[df['hemisphere'] == 'north']

        actuals = df[df['year'] == year + 1].sample(num_samples)['seq_list'].values
        actuals = np.array(actuals.tolist())
        return self.get_dist_matrix(predictions, actuals), predictions, actuals
