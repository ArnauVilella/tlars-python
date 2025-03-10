import numpy as np
import matplotlib.pyplot as plt
from tlars import TLARS, generate_gaussian_data

print("Testing TLARS package version 0.6.1")

# Generate synthetic data
print("Generating synthetic data...")
n, p = 100, 20
result = generate_gaussian_data(n=n, p=p, seed=42)
print(f"Generated data result type: {type(result)}")
# Generate our own data instead
print("Creating our own data...")
X = np.random.randn(n, p)
beta = np.zeros(p)
beta[:5] = np.array([1.5, 0.8, 2.0, -1.0, 1.2])
y = X @ beta + 0.5 * np.random.randn(n)
print(f"Generated data with {n} samples and {p} features")
print(f"True beta shape: {beta.shape}")

# Create dummy variables
print("\nCreating dummy variables...")
num_dummies = 5
dummies = np.random.randn(n, num_dummies)
XD = np.hstack([X, dummies])
print(f"Combined data shape: {XD.shape}")

# Create and fit the model
print("\nFitting TLARS model...")
model = TLARS(XD, y, num_dummies=num_dummies, verbose=True)
model.fit(T_stop=2, early_stop=True)

# Print results
print("\nResults:")
print(f"Number of active predictors: {model.n_active_}")
print(f"Number of active dummies: {model.n_active_dummies_}")
print(f"R² values: {model.r2_[-1]}")
print(f"Coefficients shape: {model.coef_.shape}")

# Test plotting
print("\nTesting plot method...")
fig = plt.figure(figsize=(10, 6))
model.plot(include_dummies=True, show_actions=True)
plt.savefig("test_plot.png")
plt.close(fig)
print("Plot saved to test_plot.png")

print("\nTest completed successfully!") 