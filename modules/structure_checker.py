import os  # provides functions to interact with the operating system


# This class will be responsible for checking whether required files and folders exist in a student’s project directory
class StructureChecker:
    def __init__(self, required_files=None, required_dirs=None):
        """
        Initializes the checker with required files and directories.
        """
        self.required_files = required_files if required_files else ["README.md"]
        self.required_dirs = required_dirs if required_dirs else ["modules"]

    def check_structure(self, project_path):
        """
        Checks whether the required files and directories are present in the given project path.
        Returns a dictionary with 'present' and 'missing' items.
        """
        present = []
        missing = []

        for item in self.required_files + self.required_dirs:
            item_path = os.path.join(project_path, item)
            if os.path.exists(item_path):
                present.append(item)
            else:
                missing.append(item)

        return {"present": present, "missing": missing}
