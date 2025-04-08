import sys
import os

# Bypass database connection
os.environ['SKIP_DB_CONNECTION'] = 'true'

# Import the CLI
from cli import main

if __name__ == '__main__':
    # Run the CLI with the lca analysis
    sys.argv = ['cli.py', 'lca']
    main()
