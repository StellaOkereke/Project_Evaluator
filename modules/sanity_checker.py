import os


class SanityChecker:
    def __init__(self, project_path):
        """
        Initializes the checker with the path to the project.
        """
        self.project_path = project_path

    def check_python_syntax(self):
        """
        Checks each Python file (.py) in the project for valid syntax.
        Returns a dictionary of passed and failed files.
        """
        passed = []
        failed = []

        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            code = f.read()
                        compile(code, file_path, "exec")  # Check syntax
                        passed.append(file_path)
                    except Exception as e:
                        failed.append((file_path, str(e)))

        return {"passed": passed, "failed": failed}
