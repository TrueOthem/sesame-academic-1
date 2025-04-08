import os
os.environ['SKIP_DB_CONNECTION'] = 'true'

try:
    import app
    print("Successfully imported app module")
except Exception as e:
    print(f"Error importing app module: {e}")
