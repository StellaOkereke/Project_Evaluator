import os

class StructureChecker:
    REQUIRED_FILES = ["README.md"]
    REQUIRED_DIRS = ["src", "tests"]

    @classmethod
    def check_structure(cls, project_path):
        present = []
        missing = []

        for item in cls.REQUIRED_FILES + cls.REQUIRED_DIRS:
            item_path = os.path.join(project_path, item)
            if os.path.exists(item_path):
                present.append(item)
            else:
                missing.append(item)

        return {"present": present, "missing": missing}
