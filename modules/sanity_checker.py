import os

class SanityChecker:
    @staticmethod
    def check_python_syntax(project_path):
        passed = []
        failed = []

        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            code = f.read()
                        compile(code, file_path, "exec")
                        passed.append(file_path)
                    except Exception as e:
                        failed.append((file_path, str(e)))

        return {"passed": passed, "failed": failed}
