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

# Override the plot method to just print the results
import core.graph
original_plot = core.graph.plot

def mock_plot(analysis_result, x, y='value', group_by=None):
    print("\n=== Analysis Results ===")
    print(f"Title: {analysis_result['title']}")
    print(f"Unit: {analysis_result['unit']}")
    print(f"Value: {analysis_result['value']}")
    print("\nData:")
    print(analysis_result['data'])
    print("\n=== End of Results ===")

core.graph.plot = mock_plot

# Run the CLI with the lca analysis
if __name__ == '__main__':
    # Set command line arguments
    sys.argv = ['cli.py', '--analysis', 'lca', '--defaults']
    
    try:
        main()
        print("CLI ran successfully!")
    except Exception as e:
        print(f"Error running CLI: {e}")
        import traceback
        traceback.print_exc()
