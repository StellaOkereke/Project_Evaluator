import streamlit as st
import tempfile
import os
from modules import Fetcher, StructureChecker, SanityChecker, ReadmeScorer

st.set_page_config(page_title="Student Project Evaluator", layout="centered")
st.title("Student Project Evaluator")

st.markdown("""
Upload a ZIP file **or** paste a GitHub URL of your Python project. This app will:
- Check project structure
- Evaluate Python code for syntax issues
- Score README.md completeness
""")

uploaded_file = st.file_uploader("Upload ZIP File", type=["zip"])
git_url = st.text_input("or Paste GitHub Repo URL")

temp_project_path = None

if st.button("Evaluate"):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
            tmp_zip.write(uploaded_file.read())
            tmp_zip_path = tmp_zip.name
        try:
            temp_project_path = Fetcher.handle_zip_upload(tmp_zip_path)
        except Exception as e:
            st.error(f"ZIP Error: {e}")
    elif git_url:
        if not git_url.startswith("https://github.com/"):
            st.error("Please enter a valid GitHub repository URL.")
        else:
            try:
                temp_project_path = Fetcher.handle_github_clone(git_url)
            except Exception as e:
                st.error(f"GitHub Clone Error: {e}")
    else:
        st.warning("Please upload a ZIP or paste a GitHub URL.")

    if temp_project_path:
        with st.expander("Structure Check"):
            structure_result = StructureChecker.check_structure(temp_project_path)
            st.write("**Present:**", structure_result['present'])
            st.write("**Missing:**", structure_result['missing'])

        with st.expander("Python Syntax Check"):
            syntax_result = SanityChecker.check_python_syntax(temp_project_path)
            st.write(f"**Passed Files ({len(syntax_result['passed'])}):**")
            st.code("\n".join(syntax_result['passed']) or "None")
            st.write(f"**Failed Files ({len(syntax_result['failed'])}):**")
            for fail in syntax_result['failed']:
                st.error(f"{fail[0]}: {fail[1]}")

        with st.expander("README Score"):
            readme_result = ReadmeScorer.score_readme(temp_project_path)
            st.write(f"**Score:** {readme_result['score']} / {readme_result['out_of']}")
            st.write("**Missing Sections:**", readme_result['missing_sections'])

        with st.expander("Final Summary"):
            total_score = readme_result['score'] + len(syntax_result['passed'])
            st.success(f"Total Score: {total_score} (syntax + readme)")

        Fetcher.cleanup_temp_dir(temp_project_path)
