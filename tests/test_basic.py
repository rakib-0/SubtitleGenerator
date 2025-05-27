"""
Basic tests for the SubtitleGenerator project.
"""

import pytest
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all main modules can be imported."""
    try:
        import transcriber
        import translator
        import formatter
        import utils
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import modules: {e}")

def test_basic_functionality():
    """Basic test to ensure the test suite works."""
    assert 1 + 1 == 2

def test_project_structure():
    """Test that required files exist."""
    project_root = os.path.join(os.path.dirname(__file__), '..')
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        '.gitignore'
    ]
    
    for file in required_files:
        file_path = os.path.join(project_root, file)
        assert os.path.exists(file_path), f"Required file {file} is missing" 