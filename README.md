# Student Project Evaluator

A Streamlit-based app that helps educators and students quickly evaluate Python projects by automating checks for:

- **Project Structure & File Naming**  
  Ensures required folders (like `src/`, `tests/`) and files (`README.md`) exist.

- **Basic Code Sanity Checks**  
  Runs syntax checks on Python files to catch errors before running code.

- **README Completeness Scoring**  
  Analyzes the README file for essential documentation sections and assigns a completeness score.

## Features

- Upload a ZIP file of your project or provide a GitHub repository URL.
- Interactive web interface built with Streamlit.
- Detailed reports for structure, code syntax, and documentation.

## How to Use

1. Clone this repo and create a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
