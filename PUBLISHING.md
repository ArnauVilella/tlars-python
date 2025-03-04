# Publishing to PyPI with GitHub Actions

This document provides detailed instructions on how to publish the `tlars` package to PyPI using GitHub Actions.

## Prerequisites

1. A GitHub account
2. A PyPI account
3. The package code pushed to a GitHub repository

## Setup Process

### 1. Create a PyPI API Token

1. Log in to your PyPI account at https://pypi.org/
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Set a token name (e.g., "GitHub Actions for tlars")
5. Select scope "Entire account (all projects)" or just the specific project if it already exists
6. Click "Create token"
7. **Important**: Copy the token immediately as you won't be able to see it again

### 2. Add the PyPI Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste the PyPI token you copied
6. Click "Add secret"

### 3. Verify GitHub Actions Workflow Files

The repository should already contain the following GitHub Actions workflow files:

- `.github/workflows/build-and-publish.yml`: Main workflow for building wheels and publishing to PyPI
- `.github/workflows/test-build.yml`: Workflow for testing the build process without publishing

If these files don't exist, you'll need to create them as described in the README.

### 4. Test the Build Process

Before publishing to PyPI, it's a good idea to test the build process:

1. Go to your repository on GitHub
2. Navigate to Actions
3. Select the "Test Build" workflow
4. Click "Run workflow"
5. Select the branch to run on (usually `main` or `master`)
6. Click "Run workflow"

This will test building the package without publishing it to PyPI.

### 5. Publishing to PyPI

To publish the package to PyPI:

1. Go to your repository on GitHub
2. Navigate to Releases
3. Click "Create a new release"
4. Set a tag version (e.g., `v0.1.0`) - make sure this matches the version in `tlars/__init__.py` and `pyproject.toml`
5. Set a release title (e.g., "Initial Release v0.1.0")
6. Add release notes describing the changes
7. Click "Publish release"

The GitHub Actions workflow will automatically trigger when you create a new release, building wheels for all platforms and publishing them to PyPI.

## Troubleshooting

### Build Failures

If the build fails, check the GitHub Actions logs for details. Common issues include:

- Missing dependencies: Make sure all dependencies are correctly specified in the workflow files
- Version mismatch: Ensure the version in `tlars/__init__.py` matches the version in `pyproject.toml`
- C++ compilation errors: Check that the C++ code compiles correctly with the specified dependencies

### Publishing Failures

If publishing fails, check:

- PyPI token: Ensure the PyPI token is correctly set in GitHub Secrets
- Package name: Make sure the package name is available on PyPI
- Version: Ensure you're not trying to publish a version that already exists on PyPI

## Updating the Package

To update the package:

1. Make your changes to the code
2. Update the version number in `tlars/__init__.py` and `pyproject.toml`
3. Commit and push your changes
4. Create a new release on GitHub with the new version number
5. The GitHub Actions workflow will automatically build and publish the new version

## Manual Publishing (if needed)

If you need to publish manually without GitHub Actions:

1. Install build tools: `pip install build twine`
2. Build the package: `python -m build`
3. Upload to PyPI: `twine upload dist/*`

However, this approach won't build wheels for all platforms, which is why using GitHub Actions with cibuildwheel is recommended. 