# tlars

Python implementation of the Truncated Least Angle Regression (TLARS) package.

## Authors

- Original R package: Jasin Machkour
- Python port: Arnau Vilella (avp@connect.ust.hk)

## Installation

### Requirements
- Python 3.7 or later
- C++ compiler with C++11 support
- NumPy
- Eigen3 (system package)
- pybind11 (system package)

### Local Installation
To install the package locally, clone this repository and run:

```bash
pip install .
```

## Usage

```python
from tlars import TLARS
import numpy as np

# Create some example data
X = np.random.randn(100, 10)
y = np.random.randn(100)

# Create and fit the model
model = TLARS()
model.fit(X, y)

# Make predictions
predictions = model.predict(X)

# Access model coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
```

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Acknowledgments

This is a Python port of the original R package `tlars` by Jasin Machkour. 