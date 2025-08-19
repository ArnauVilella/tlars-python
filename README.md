# tlars-python

A Python port of the [tlars](https://github.com/cran/tlars) R package for Terminating-LARS (T-LARS) algorithm.

## Overview

The Terminating-LARS (T-LARS) algorithm is a modification of the Least Angle Regression (LARS) algorithm that allows for early termination of the forward selection process. This is particularly useful for high-dimensional data where the number of predictors is much larger than the number of observations.

This Python package provides a port of the original R implementation by Jasin Machkour, maintaining the same functionality while providing a more Pythonic interface. The Python port was created by Arnau Vilella (avp@connect.ust.hk).

## Installation

The package is available on PyPI for Windows, macOS, and Linux:

```bash
pip install tlars
```

This is the recommended installation method as it will automatically install pre-built wheels for your platform with all required dependencies.

## Usage

```python
import numpy as np
from tlars import TLARS, generate_gaussian_data

# Generate some example data using the built-in function
n, p = 100, 20
X, y, beta = generate_gaussian_data(n=n, p=p, seed=42)

# Alternatively, create your own data
X = np.random.randn(n, p)
beta = np.zeros(p)
beta[:5] = np.array([1.5, 0.8, 2.0, -1.0, 1.2])
y = X @ beta + 0.5 * np.random.randn(n)

# Create dummy variables
num_dummies = p
dummies = np.random.randn(n, num_dummies)
XD = np.hstack([X, dummies])

# Create and fit the model
model = TLARS(XD, y, num_dummies=num_dummies)
model.fit(T_stop=3, early_stop=True)

# Get the coefficients
print(model.coef_)

# Get other properties
print(f"Number of active predictors: {model.n_active_}")
print(f"Number of active dummies: {model.n_active_dummies_}")
print(f"R² values: {model.r2_}")

# Plot the solution path
model.plot(include_dummies=True, show_actions=True)
```

## Library Reference

### TLARS Class

#### Constructor

```python
TLARS(X=None, y=None, verbose=False, intercept=True, standardize=True, 
      num_dummies=0, type='lar', lars_state=None, info=True)
```

- **X**: numpy.ndarray - Real valued predictor matrix.
- **y**: numpy.ndarray - Response vector.
- **verbose**: bool - If True, progress in computations is shown.
- **intercept**: bool - If True, an intercept is included.
- **standardize**: bool - If True, the predictors are standardized and the response is centered.
- **num_dummies**: int - Number of dummies that are appended to the predictor matrix.
- **type**: str - Type of used algorithm (currently possible choices: 'lar' or 'lasso').
- **lars_state**: object - Previously saved TLARS state to resume from.
- **info**: bool - If True, information about the initialization is printed.

#### Methods

- **fit(T_stop=None, early_stop=True, info=True)**: Fit the TLARS model.
  - **T_stop**: int - Number of included dummies after which the random experiments are stopped.
  - **early_stop**: bool - If True, then the forward selection process is stopped after T_stop dummies have been included.
  - **info**: bool - If True, informational messages are displayed during fitting.

- **plot(xlabel="# Included dummies", ylabel="Coefficients", include_dummies=True, show_actions=True, col_selected="black", col_dummies="red", ls_selected="-", ls_dummies="--", legend_pos="best", figsize=(10, 6))**: Plot the T-LARS solution path.
  - **xlabel**: str - Label for the x-axis.
  - **ylabel**: str - Label for the y-axis.
  - **include_dummies**: bool - If True, solution paths of dummies are added to the plot.
  - **show_actions**: bool - If True, marks for added variables are shown above the plot.
  - **col_selected**: str - Color of lines corresponding to selected variables.
  - **col_dummies**: str - Color of lines corresponding to dummy variables.
  - **ls_selected**: str - Line style for selected variables.
  - **ls_dummies**: str - Line style for dummy variables.
  - **legend_pos**: str - Position of the legend.
  - **figsize**: tuple - Figure size.

- **get_all()**: Returns a dictionary with all the results and properties.

#### Properties

- **coef_**: numpy.ndarray - The coefficients of the model.
- **coef_path_**: list - A list of coefficient vectors at each step.
- **n_active_**: int - The number of active predictors.
- **n_active_dummies_**: int - The number of active dummy variables.
- **n_dummies_**: int - The total number of dummy variables.
- **actions_**: list - The indices of added/removed variables along the solution path.
- **df_**: list - The degrees of freedom at each step.
- **r2_**: list - The R² statistic at each step.
- **rss_**: list - The residual sum of squares at each step.
- **cp_**: numpy.ndarray - The Cp-statistic at each step.
- **lambda_**: numpy.ndarray - The lambda-values (penalty parameters) at each step.
- **entry_**: list - The first entry/selection steps of the predictors.

### Helper Functions

- **generate_gaussian_data(n=50, p=100, seed=789)**: Generate synthetic Gaussian data for testing.
  - **n**: int - Number of observations.
  - **p**: int - Number of variables.
  - **seed**: int - Random seed for reproducibility.
  - **Returns**: tuple - (X, y, beta) where X is the design matrix, y is the response, and beta is the true coefficient vector.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

## Acknowledgments

The original R package [tlars](https://github.com/cran/tlars) was created by Jasin Machkour. This Python port was developed by Arnau Vilella (avp@connect.ust.hk). 