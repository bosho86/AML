from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class heartrate(BaseEstimator, TransformerMixin):
    """heartrate"""
    def __init__(self, NfeaMax=None,
                 is_moving=True,
                 moving_method='average',
                 Nwins=100,
                 is_correlation=True,
                 timeint_start=1,
                 timeint_dt=10,
                 timeint_last=1000):
        self.NfeaMax = NfeaMax
        self.is_moving = is_moving
        self.moving_method = moving_method
        self.Nwins = Nwins
        self.is_correlation = is_correlation
        self.timeint_start = timeint_start
        self.timeint_dt = timeint_dt
        self.timeint_last = timeint_last

    def fit(self, X, y=None):
        print("heartrate")
        print(X.shape)
        print("    Nothing is done here")
        return self

    def data_moving(self, X):
        Nwins = self.Nwins
        moving_method = self.moving_method
        n_samples, n_f = X.shape
        moving = np.zeros((n_samples, n_f-(Nwins-1)), dtype="float")
        ii = -1
        for i in np.arange((Nwins-1), n_f):
            ii = ii + 1
            indi = i-(Nwins-1)
            indf = i+1
            if moving_method == 'average':
                moving[:, ii] = np.sum(X[:, indi:indf], axis=1)/Nwins
            elif moving_method == 'median':
                moving[:, ii] = np.median(X[:, indi:indf], axis=1)
        return moving

    def data_analyze(self, X):
        n_samples, n_f = X.shape
        N_Xlast = np.zeros((n_samples, ), dtype="int")
        X_m = np.zeros((n_samples, ), dtype="float")
        X_std = np.zeros((n_samples, ), dtype="float")
        for i in np.arange(n_samples):
            train = X[i, :]
            for itr in np.arange(n_f-1, 1, -1):
                if train[itr] != 0.0:
                    N_Xlast[i] = itr
                    break
            train = train[0:(N_Xlast[i]+1)]
            X_m[i] = np.mean(train)
            X_std[i] = np.std(train)
        return N_Xlast, X_m, X_std

    def transform(self, X, y=None):
        print(X.shape)
        if self.NfeaMax is not None:
            X = X[:, 0:self.NfeaMax]
        print(X.shape)
        if self.is_moving is True:
            X = self.data_moving(X)
        print(X.shape)
        if self.is_correlation is True:
            print("p")
            itrval = np.arange(self.timeint_start,
                               self.timeint_last+1,
                               self.timeint_dt)
            N_Xlast, X_m, X_std = self.data_analyze(X)
            n_samples, n_f = X.shape
            for i in np.arange(n_samples):
                ir = np.arange(N_Xlast[i]+1)
                perro = np.zeros((len(ir), ), dtype='float')
            X[i, ir] = X[i, ir] - (X_m[i] + perro)
            X_new = np.zeros((n_samples, len(itrval)), dtype="float")
            ii = -1
            for it in itrval:
                ii = ii + 1
                if np.remainder(ii, 500) == 0:
                    print(it)
                nm = (N_Xlast+1-it).astype('float')*X_std**2
            X_new[:, ii] = np.sum(X[:, 0:(n_f-it)] * X[:, it:n_f], axis=1) / nm
            X = X_new
            print(X.shape)
        return X
