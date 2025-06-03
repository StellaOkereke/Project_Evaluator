# Import required libraries and modules
import streamlit as st  # Streamlit for UI components and web app
import tempfile  # For creating temporary directories/files
import os  # For file path operations
from modules import Fetcher, StructureChecker, SanityChecker, ReadmeScorer


# Create instances of your classes
fetcher = Fetcher()
structure_checker = StructureChecker()
# sanity_checker = SanityChecker()
readme_scorer = ReadmeScorer()

st.markdown(
    """
<style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
    }
    h1 {
        color: #1f77b4 !important;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #ff7f0e !important;
    }
    h3 {
        color: #2ca02c !important;
    }
    .st-expander > summary {
        font-size: 18px;
        font-weight: bold;
        color: #3366cc;
    }
    .final-summary {
        background-color: #1f77b4;
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Student Project Evaluator")

repo_url = st.text_input("Enter GitHub Repo URL")
zip_file = st.file_uploader("Upload ZIP of your project", type="zip")

if st.button("Evaluate"):
    project_path = None

    if zip_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
            tmp_zip.write(zip_file.read())
            tmp_zip_path = tmp_zip.name

        project_path = fetcher.handle_zip_upload(tmp_zip_path)
        st.success("ZIP uploaded and extracted successfully!")

    elif repo_url:
        project_path = fetcher.handle_github_clone(repo_url)
        st.success("GitHub repo cloned successfully!")

    else:
        st.error("Please upload a ZIP file or enter a GitHub repository URL.")

    if project_path:
        sanity_checker = SanityChecker(project_path)
        structure_result = structure_checker.check_structure(project_path)
        readme_result = readme_scorer.score(project_path)
        syntax_result = sanity_checker.check_python_syntax()

        # STRUCTURE RESULT
        with st.expander("📁 Structure Check"):
            st.markdown("### ✅ Present Files")
            st.write(structure_result["present"])
            st.markdown("### ❌ Missing Files")
            st.write(structure_result["missing"])

        # README SCORE
        with st.expander("📘 README Score"):
            st.markdown(f"### Score: `{readme_result['score']} / 4`")
            st.markdown("### ❌ Missing Sections")
            st.write(readme_result["missing"])

        # SANITY RESULT
        with st.expander("🧪 Sanity Check Results"):
            st.markdown("### ✅ Passed Files")
            st.write(syntax_result["passed"])

            st.markdown("### ❌ Failed Files")
            if syntax_result["failed"]:
                for error in syntax_result["failed"]:
                    st.error(error)
            else:
                st.write("No syntax errors detected.")

        # FINAL SCORE SUMMARY
        total_possible_score = (
            4 + len(syntax_result["passed"]) + len(syntax_result["failed"])
        )
        total_score = readme_result["score"] + len(syntax_result["passed"])

        st.markdown(
            f"""
            <div class="final-summary">
                🎯 Total Score: {total_score} / {total_possible_score} <br>
                ✅ Syntax Passed: {len(syntax_result['passed'])} <br>
                ❌ Syntax Failed: {len(syntax_result['failed'])} <br>
                📄 README Score: {readme_result['score']} / 4
            </div>
            """,
            unsafe_allow_html=True,
        )
