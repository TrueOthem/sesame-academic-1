import sys
import os

# Set environment variables
os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Import the CLI
from cli import LCACLI, main

# Override the prompt_options function to always return the first option
import cli
original_prompt_options = cli.prompt_options

def mock_prompt_options(options, label):
    print(f"Mocked prompt for {label}: returning {options[0]}")
    return options[0]

cli.prompt_options = mock_prompt_options

# Override the prompt_value function to always return the default value
original_prompt_value = cli.prompt_value

def mock_prompt_value(user_input, input_set):
    default = input_set.default_value(user_input.name)
    print(f"Mocked prompt for {user_input.name}: returning {default}")
    return default if default is not None else 0.0

cli.prompt_value = mock_prompt_value

# Run the CLI with the lca analysis
if __name__ == '__main__':
    # Set command line arguments
    sys.argv = ['cli.py', '--analysis', 'lca', '--defaults']
    
    try:
        main()
    except Exception as e:
        print(f"Error running CLI: {e}")
        import traceback
        traceback.print_exc()
