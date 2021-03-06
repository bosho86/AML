from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array
import numpy as np
import peakutils
from biosppy.signals import ecg
from scipy.signal import butter, lfilter


class ecg_preprocessing(BaseEstimator, TransformerMixin):
    """support vector machine"""
    def _init_(self, dim=300):
        self.dim = dim
        return self

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = check_array(X)
        X = ecg.christov_segmenter(signal=X, sampling_rate=300)
        print('some stdout')
        return X


class Flatten(BaseEstimator, TransformerMixin):
    """Flatten"""
    def __init__(self, dim=2):
        self.dim = dim

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = check_array(X)
        X = X.reshape(-1, 176, 208, 176)
        X = X.mean(axis=self.dim)
        print('some stdout')
        return X.reshape(X.shape[0], -1)


class Filter(BaseEstimator, TransformerMixin):
    """Filter"""
    def __init__(self, dim=2):
        self.dim = dim

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = check_array(X)
        nyq = 0.5 * 300
        lowcut = 16
        highcut = 50
        low = lowcut / nyq
        high = highcut / nyq
        order = 9
        b, a = butter(order, [low, high], btype='band')
        X = lfilter(b, a, X)
        print('some stdout')
        return X


class peaks(BaseEstimator, TransformerMixin):
    """Filter"""
    def __init__(self, dim=2):
        self.dim = dim

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = check_array(X)
        X = peakutils.indexes(X, thres=0.5, min_dist=30)
        print('some stdout')
        return X


class FFT(BaseEstimator, TransformerMixin):
    """Filter"""
    def __init__(self, dim=2):
        self.dim = dim

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = check_array(X)
        X = np.fft.fft(X, axis=-1)
        print('some stdout')
        return X


class IFFT(BaseEstimator, TransformerMixin):
    """Filter"""
    def __init__(self, dim=2):
        self.dim = dim

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = check_array(X)
        X = np.fft.ifft(X, axis=-1)
        print('some stdout')
        return X
