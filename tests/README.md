# TLARS Tests

This directory contains tests for the TLARS Python package. The tests are written using the pytest framework.

## Running the Tests

To run all tests, navigate to the main package directory and run:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_tlars.py
```

To run a specific test case:

```bash
pytest tests/test_tlars.py::test_tlars_finds_true_coefficients
```

## Test Files

- `test_tlars.py`: Tests for the primary TLARS functionality and algorithm.
- `test_tlars_model.py`: Tests for the TLARS model state and lifecycle functionality.
- `conftest.py`: Configuration for pytest and common fixtures.

## Requirements

The tests require:
- pytest
- numpy
- matplotlib

Install with:

```bash
pip install pytest numpy matplotlib
``` 