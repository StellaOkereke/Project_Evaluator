import os
import ast  # Abstract Syntax Trees module for parsing Python source code and detecting syntax errors


class SanityChecker:
    """
    Class to perform syntax checking of Python files in a given directory.
    """

    def __init__(self, project_path):
        self.project_path = project_path

    def check_python_syntax(self):
        """
        Walks through all Python files in the directory tree rooted at `path`.
        For each `.py` file, attempts to parse the file's source code to detect
        any Python syntax errors.

        Args:
            path (str): Root directory path of the project to check.

        Returns:
            dict: Contains two keys:
                - "passed": list of relative file paths that passed syntax check.
                - "failed": list of dicts with keys "file" and "error" for files
                  that failed syntax check.
        """
        result = {"passed": [], "failed": []}
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            source = f.read()
                            ast.parse(source)
                        result["passed"].append(
                            os.path.relpath(full_path, self.project_path)
                        )
                    except SyntaxError:
                        result["failed"].append(
                            os.path.relpath(full_path, self.project_path)
                        )
        return result
