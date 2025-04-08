# SESAME Academic

SESAME Academic is a Python-based framework for sustainability analysis, focusing on lifecycle assessment (LCA) and techno-economic analysis (TEA) of various energy pathways.

## Overview

This repository contains the core libraries and tools for performing sustainability analyses, including:

- Lifecycle assessment (LCA) for environmental impact analysis
- Techno-economic analysis (TEA) for economic feasibility assessment
- System-level analyses for fleet, grid, and other complex systems
- Command-line interface (CLI) for running analyses

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sesame-sustainability/sesame-academic.git
   cd sesame-academic
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The primary way to interact with SESAME Academic is through the command-line interface:

```bash
python cli.py --analysis <analysis_type> [--defaults] [--input <input_file>] [--output <output_file>] [--group-by <group_by>]
```

Where:
- `<analysis_type>` can be one of: lca, tea, fleet, grid, pps, cement, steel, aluminum, industrial_fleet
- `--defaults` uses default inputs instead of prompting
- `--input` specifies a JSON file containing inputs
- `--output` specifies a JSON file to store collected inputs
- `--group-by` specifies how to group results (default=pathway)

### Example

Run an LCA analysis with default values:

```bash
python cli.py --analysis lca --defaults
```

## Database Configuration

SESAME Academic can work with a PostgreSQL database or fall back to SQLite. To configure the database connection, set the following environment variables:

```bash
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=sesame
```

If these variables are not set, the system will use a local SQLite database.

## Development

### Running Tests

```bash
python -m pytest
```

### Code Structure

- `core/`: Core functionality and data models
- `analysis/`: Analysis modules for different types of assessments
- `pathway/`: Pathway definitions and implementations
- `tea/`: Techno-economic analysis modules
- `cli.py`: Command-line interface

## License

This project is licensed under the terms of the license included in the repository.

## Acknowledgements

SESAME Academic is developed by the SESAME Sustainability team.
