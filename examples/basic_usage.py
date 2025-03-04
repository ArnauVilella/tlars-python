import numpy as np
from tlars import TLARS

# Generate some example data
np.random.seed(42)
n_samples, n_features = 100, 20
X = np.random.randn(n_samples, n_features)

# Create true coefficients with only a few non-zero elements
true_coef = np.zeros(n_features)
true_coef[:3] = [1.0, -1.0, 0.5]

# Generate target values with noise
y = np.dot(X, true_coef) + 0.1 * np.random.randn(n_samples)

# Create and fit the TLARS model
model = TLARS()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Print results
print("True coefficients:", true_coef)
print("\nEstimated coefficients:", model.coef_)
print("\nIntercept:", model.intercept_)
print("\nMean squared error:", np.mean((y - y_pred) ** 2))

# Test on new data
X_test = np.random.randn(10, n_features)
y_test_pred = model.predict(X_test)
print("\nPredictions on new data:", y_test_pred) 