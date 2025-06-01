import os


class ReadmeScorer:
    def __init__(self, required_sections=None):
        """
        Initializes the scorer with a list of required README sections.
        """
        if required_sections is None:
            required_sections = [
                "# Introduction",
                "# Installation",
                "# Usage",
                "# License",
            ]
        self.required_sections = required_sections

    def score(self, project_path):
        """
        Scores the README.md file by checking if required sections are present.
        Returns a dictionary with score and missing sections.
        """
        readme_path = os.path.join(project_path, "README.md")

        if not os.path.exists(readme_path):
            return {"score": 0, "missing": self.required_sections}

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        missing_sections = [
            section for section in self.required_sections if section not in content
        ]
        score = len(self.required_sections) - len(missing_sections)

        return {"score": score, "missing": missing_sections}
