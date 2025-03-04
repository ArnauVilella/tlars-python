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

## Publishing to PyPI with GitHub Actions

This package uses GitHub Actions to automatically build and publish to PyPI. The workflow is configured to:

1. Build wheels for Linux, macOS, and Windows using cibuildwheel
2. Build a source distribution
3. Publish to PyPI when a new release is created

### Setup for Publishing

To set up publishing to PyPI:

1. Create an API token on PyPI:
   - Go to https://pypi.org/manage/account/
   - Create an API token with scope "Upload to PyPI"
   - Copy the token value

2. Add the token as a secret in your GitHub repository:
   - Go to your repository on GitHub
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste the token you copied from PyPI
   - Click "Add secret"

3. Create a new release on GitHub:
   - Go to your repository on GitHub
   - Navigate to Releases
   - Click "Create a new release"
   - Set a tag version (e.g., v0.1.0)
   - Set a release title
   - Click "Publish release"

The GitHub Actions workflow will automatically trigger when you create a new release, building wheels for all platforms and publishing them to PyPI.

### Manual Triggering

You can also manually trigger the build process without publishing to PyPI:

1. Go to your repository on GitHub
2. Navigate to Actions
3. Select the "Build and Publish" workflow
4. Click "Run workflow"
5. Select the branch to run on
6. Click "Run workflow"

This will build the wheels but won't publish them to PyPI unless it was triggered by a release. 