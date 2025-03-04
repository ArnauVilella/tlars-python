import numpy as np
import pytest
from tlars import TLARS

def test_tlars_initialization():
    model = TLARS()
    assert model.coef_ is None
    assert model.intercept_ is None

def test_tlars_input_validation():
    model = TLARS()
    X = np.random.randn(100, 10)
    y = np.random.randn(100)
    
    # Test wrong dimensions
    with pytest.raises(ValueError):
        model.fit(X.reshape(-1), y)  # 1D X
    
    with pytest.raises(ValueError):
        model.fit(X, y.reshape(-1, 1))  # 2D y
    
    # Test mismatched dimensions
    with pytest.raises(ValueError):
        model.fit(X, y[:-1])  # Different number of samples

def test_tlars_predict_before_fit():
    model = TLARS()
    X = np.random.randn(100, 10)
    
    with pytest.raises(RuntimeError):
        model.predict(X)

def test_tlars_predict_input_validation():
    # Create and fit model first
    model = TLARS()
    X = np.random.randn(100, 10)
    y = np.random.randn(100)
    model.fit(X, y)
    
    # Test prediction with wrong dimensions
    with pytest.raises(ValueError):
        model.predict(X.reshape(-1))  # 1D X

def test_tlars_basic_workflow():
    # Create simple test data
    n_samples, n_features = 100, 10
    X = np.random.randn(n_samples, n_features)
    true_coef = np.zeros(n_features)
    true_coef[:3] = [1.0, -1.0, 0.5]  # Only first three features are relevant
    y = np.dot(X, true_coef) + 0.1 * np.random.randn(n_samples)
    
    # Fit model
    model = TLARS()
    model.fit(X, y)
    
    # Basic checks
    assert model.coef_ is not None
    assert model.intercept_ is not None
    assert len(model.coef_) == n_features
    
    # Test prediction shape
    predictions = model.predict(X)
    assert predictions.shape == (n_samples,)
    
    # Test with new data
    X_new = np.random.randn(50, n_features)
    predictions_new = model.predict(X_new)
    assert predictions_new.shape == (50,) 