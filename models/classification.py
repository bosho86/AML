import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import svm
from sklearn.utils.validation import check_array, check_is_fitted
from sklearn.ensemble import RandomForestClassifier


class MeanPredictor(BaseEstimator, TransformerMixin):
    """docstring for MeanPredictor"""
    def fit(self, X, y):
        self.mean = y.mean(axis=0)
        return self

    def predict_proba(self, X):
        check_array(X)
        check_is_fitted(self, ["mean"])
        n_samples, _ = X.shape
        return np.tile(self.mean, (n_samples, 1))


class SVM(BaseEstimator, TransformerMixin):
    """support vector machine"""
    def _init_(self, cl):
        self.cl = None
        return self

    def fit(self, X, y):
        self.cl = svm.SVC(decision_function_shape='ovo', probability=True)
        self.cl.fit(X, y)
        return self

    def predict_proba(self, X):
        return self.cl.predict_proba(X)


class RF(BaseEstimator, TransformerMixin):
    """support vector machine"""
    def _init_(self, cl):
        self.cl = None
        return self

    def fit(self, X, y):
        self.cl = RandomForestClassifier(n_estimators=120)
        self.cl.fit(X, y)
        return self

    def predict(self, X):
        out = self.cl.predict(X)
        return out.astype('int')
