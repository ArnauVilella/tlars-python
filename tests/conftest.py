"""
Configuration file for pytest.
"""
import os
import sys

# Add the parent directory to the Python path
# This ensures that the tlars package is importable during testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 