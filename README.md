# tlars-python

A Python port of the [tlars](https://github.com/cran/tlars) R package for Terminating-LARS (T-LARS) algorithm.

## Overview

The Terminating-LARS (T-LARS) algorithm is a modification of the Least Angle Regression (LARS) algorithm that allows for early termination of the forward selection process. This is particularly useful for high-dimensional data where the number of predictors is much larger than the number of observations.

This Python package provides a port of the original R implementation by Jasin Machkour, maintaining the same functionality while providing a more Pythonic interface. The Python port was created by Arnau Vilella (avp@connect.ust.hk).

## Installation

### Prerequisites

- Python 3.6+
- NumPy
- A C++ compiler (GCC, Clang, MSVC, etc.)
- Armadillo C++ library

### Installing Armadillo

#### Ubuntu/Debian
```bash
sudo apt-get install libarmadillo-dev
```

#### macOS
```bash
brew install armadillo
```

#### Windows
For Windows, you may need to download and build Armadillo from source: http://arma.sourceforge.net/download.html

### Installing the package

#### From PyPI
```bash
# First install the armadillo dependency
# Ubuntu/Debian:
sudo apt-get install libarmadillo-dev

# macOS:
# brew install armadillo

# Then install the package
pip install tlars
```

#### From source
```bash
# Install the armadillo dependency first
# Ubuntu/Debian:
sudo apt-get install libarmadillo-dev
# macOS:
# brew install armadillo

# Clone the repository
git clone https://github.com/ArnauVilella/tlars-python-2.git
cd tlars-python-2

# Initialize and update submodules
git submodule init
git submodule update

# Install the package
pip install -e .
```

## Usage

```python
import numpy as np
from tlars import TLARS

# Generate some example data
n, p = 100, 20
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
```

## API Reference

### TLARS Class

#### Constructor

```python
TLARS(X, y, verbose=False, intercept=True, standardize=True, num_dummies=0, type='lar')
```

- **X**: numpy.ndarray - Real valued predictor matrix.
- **y**: numpy.ndarray - Response vector.
- **verbose**: bool - If True, progress in computations is shown.
- **intercept**: bool - If True, an intercept is included.
- **standardize**: bool - If True, the predictors are standardized and the response is centered.
- **num_dummies**: int - Number of dummies that are appended to the predictor matrix.
- **type**: str - Type of used algorithm (currently possible choices: 'lar' or 'lasso').

#### Methods

- **fit(T_stop=None, early_stop=True)**: Fit the TLARS model.
  - **T_stop**: int - Number of included dummies after which the random experiments are stopped.
  - **early_stop**: bool - If True, then the forward selection process is stopped after T_stop dummies have been included.

#### Properties

- **coef_**: numpy.ndarray - The coefficients of the model.
- **coef_path_**: list - A list of coefficient vectors at each step.
- **n_active_**: int - The number of active predictors.
- **n_active_dummies_**: int - The number of active dummy variables.
- **actions_**: list - The indices of added/removed variables along the solution path.
- **df_**: list - The degrees of freedom at each step.
- **r2_**: list - The R² statistic at each step.
- **rss_**: list - The residual sum of squares at each step.
- **cp_**: numpy.ndarray - The Cp-statistic at each step.
- **lambda_**: numpy.ndarray - The lambda-values (penalty parameters) at each step.
- **entry_**: list - The first entry/selection steps of the predictors.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

## Acknowledgments

The original R package [tlars](https://github.com/cran/tlars) was created by Jasin Machkour. This Python port was developed by Arnau Vilella (avp@connect.ust.hk). 