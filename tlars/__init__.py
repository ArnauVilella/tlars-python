"""
tlars: Python implementation of the tlars package

This package is a Python port of the R package 'tlars' originally developed by Jasin Machkour.
Python implementation by Arnau Vilella (avp@connect.ust.hk).

The package implements the Truncated Least Angle Regression algorithm for high-dimensional
statistical learning.
"""

__version__ = "0.1.3"

from ._tlars_cpp import TLARS as _TLARS
import numpy as np

class TLARS:
    """
    Truncated Least Angle Regression implementation in Python.
    This class provides a scikit-learn compatible interface to the C++ implementation.
    """
    
    def __init__(self):
        """Initialize the TLARS model."""
        self._model = _TLARS()
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        Fit the TLARS model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
            
        Returns
        -------
        self : object
            Returns self.
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        
        if X.ndim != 2:
            raise ValueError("X must be a 2-D array")
        if y.ndim != 1:
            raise ValueError("y must be a 1-D array")
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples")
            
        self._model.fit(X, y)
        self.coef_ = self._model.get_coefficients()
        self.intercept_ = self._model.get_intercept()
        return self

    def predict(self, X):
        """
        Predict using the TLARS model.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples
            
        Returns
        -------
        y_pred : array-like of shape (n_samples,)
            Returns predicted values.
        """
        if self.coef_ is None:
            raise RuntimeError("Call fit before predicting")
            
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2:
            raise ValueError("X must be a 2-D array")
            
        return self._model.predict(X) 