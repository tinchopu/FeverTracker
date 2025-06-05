#!/usr/bin/env python3
"""
Test script to verify the Fever Tracker application works correctly with uv.
"""

import sys
from datetime import datetime
import pytz

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import streamlit: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pandas: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✓ Plotly imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import plotly: {e}")
        return False
    
    try:
        import pytz
        print("✓ Pytz imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pytz: {e}")
        return False
    
    return True

def test_core_functionality():
    """Test core application functionality."""
    print("\nTesting core functionality...")
    
    try:
        # Test utils module
        from utils import load_data, add_temperature, create_temperature_chart
        print("✓ Utils module imported successfully")
        
        # Test loading data (should create empty DataFrame if no file exists)
        df = load_data()
        print(f"✓ Data loading works (loaded {len(df)} records)")
        
        # Test adding temperature
        timestamp = datetime.now(pytz.UTC)
        df = add_temperature(37.2, timestamp, "Test medication", df)
        print(f"✓ Temperature addition works (now {len(df)} records)")
        
        # Test chart creation
        if len(df) > 0:
            fig = create_temperature_chart(df)
            print("✓ Chart creation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Core functionality test failed: {e}")
        return False

def test_style_module():
    """Test style module."""
    print("\nTesting style module...")
    
    try:
        from style import apply_custom_style
        print("✓ Style module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import style module: {e}")
        return False

def main():
    """Run all tests."""
    print("🌡️ Fever Tracker - Testing with UV Environment")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test core functionality
    if not test_core_functionality():
        all_tests_passed = False
    
    # Test style module
    if not test_style_module():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! The application is ready to use with uv.")
        print("\nTo start the application, run:")
        print("  make run")
        print("\nOr manually:")
        print("  uv run streamlit run main.py --server.port 8501")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
