# Publishing to PyPI

This document outlines the steps to publish the tlars package to PyPI using GitHub Actions.

## Prerequisites

1. A PyPI account
2. API token from PyPI
3. GitHub repository with the tlars-python code

## Setting up the PyPI API Token in GitHub

1. Generate a PyPI API token:
   - Go to https://pypi.org/manage/account/
   - Click on "Add API token"
   - Give the token a name (e.g. "GitHub Actions for tlars")
   - Set the scope to "Entire account" or only the tlars project
   - Click "Add token" and copy the token value (you won't be able to see it again)

2. Add the token as a GitHub secret:
   - Go to your GitHub repository
   - Click on "Settings" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name it `PYPI_API_TOKEN`
   - Paste the token value you copied
   - Click "Add secret"

## Publishing a new release

1. Update version number in:
   - `setup.py` (__version__ variable)
   - `pyproject.toml` (version field)

2. Create a new GitHub release:
   - Go to your GitHub repository
   - Click on "Releases" > "Create a new release"
   - Create a new tag (e.g. "v1.0.0")
   - Title the release (e.g. "tlars 1.0.0")
   - Add release notes
   - Click "Publish release"

3. Monitor the GitHub Action:
   - Go to "Actions" tab in your repository
   - You should see the "Python Package Build and Publish" workflow running
   - Once completed, your package will be available on PyPI

The workflow will:
1. Build manylinux-compatible binary wheels for various Python versions
2. Build a source distribution
3. Upload both wheels and source distribution to PyPI when triggered by a release

## Testing the build process

You can test the build process without publishing to PyPI:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Python Package Build and Publish" workflow
3. Click on "Run workflow" > "Run workflow" (green button)
4. This will run all the build steps but will NOT publish to PyPI

## Troubleshooting

If the GitHub Action fails:
1. Check the action logs for error messages
2. Ensure all dependencies are correctly specified
3. Verify that the build is successful locally before pushing to GitHub
4. Make sure the PyPI API token is correctly set up as a GitHub secret 