import os

class ReadmeScorer:
    SECTIONS = ["# Introduction", "# Installation", "# Usage", "# License"]

    @classmethod
    def score_readme(cls, project_path):
        readme_path = os.path.join(project_path, "README.md")
        if not os.path.exists(readme_path):
            return {"score": 0, "out_of": len(cls.SECTIONS), "missing_sections": cls.SECTIONS}

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        score = 0
        missing = []
        for section in cls.SECTIONS:
            if section.lower() in content:
                score += 1
            else:
                missing.append(section)

        return {"score": score, "out_of": len(cls.SECTIONS), "missing_sections": missing}
