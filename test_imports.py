# Test basic imports
try:
    import matplotlib
    import numpy
    import pandas
    print("Basic scientific libraries imported successfully")
except ImportError as e:
    print(f"Error importing scientific libraries: {e}")

# Try to import from the project
try:
    import core.common
    print("Core module imported successfully")
except ImportError as e:
    print(f"Error importing core module: {e}")

print("Import test completed")
