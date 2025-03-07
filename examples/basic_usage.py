import numpy as np
import matplotlib.pyplot as plt
from tlars import TLARS, gaussian_data

# Use the included Gaussian data example
X = gaussian_data['X']
y = gaussian_data['y']
true_beta = gaussian_data['beta']
p = X.shape[1]
n = X.shape[0]

print(f"Data dimensions: n={n}, p={p}")
print(f"True non-zero coefficients: {np.where(true_beta != 0)[0] + 1}")

# Create dummy variables
num_dummies = p
np.random.seed(42)  # For reproducibility
dummies = np.random.randn(n, num_dummies)
XD = np.hstack([X, dummies])

print(f"Data with dummies shape: {XD.shape}")

# Create a TLARS model
model = TLARS(X=XD, y=y, num_dummies=num_dummies, verbose=True)

# Fit the model with early stopping
T_stop = 3  # Stop after including 3 dummies
model.fit(T_stop=T_stop, early_stop=True)

# Print model information
print("\nModel summary:")
print(model)

# Get coefficients
beta = model.coef_
print("\nEstimated coefficients:")
non_zero_indices = np.where(np.abs(beta[:p]) > 1e-10)[0]
if len(non_zero_indices) > 0:
    for idx in non_zero_indices:
        print(f"  Variable {idx+1}: {beta[idx]:.4f}")
else:
    print("  No non-zero coefficients")

# Plot the solution path
fig, ax = model.plot(figsize=(12, 6))
plt.title("TLARS Solution Path")
plt.savefig("tlars_solution_path.png")
plt.show()

# Access some model properties
print("\nModel properties:")
print(f"  Number of active predictors: {model.n_active_}")
print(f"  Number of active dummies: {model.n_active_dummies_}")
print(f"  R² values: {model.r2_}")
print(f"  Actions (selected variables): {model.actions_}")

# Compute the full solution path
print("\nComputing full solution path...")
model_full = TLARS(X=XD, y=y, num_dummies=num_dummies)
model_full.fit(early_stop=False)

print(f"  Solution path length: {len(model_full.coef_path_)}")
print(f"  Number of active predictors: {model_full.n_active_}")

# Plot the full solution path
fig, ax = model_full.plot(figsize=(12, 6))
plt.title("Full TLARS Solution Path")
plt.savefig("tlars_full_solution_path.png")
plt.show()

# Demonstrating warm restart with lars_state
print("\nDemonstrating warm restart:")
state = model.get_all()
new_model = TLARS(lars_state=state)
print(f"  Original model active predictors: {model.n_active_}")
print(f"  New model active predictors: {new_model.n_active_}")
print("  Models match:", model.n_active_ == new_model.n_active_) 