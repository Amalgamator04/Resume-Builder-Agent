import streamlit as st
import os
from pathlib import Path
from components.llm_summary import get_llm_summary
from components.llm_skills import get_llm_skills
from components.llm_projects import get_llm_projects
from main import create_resume

# Streamlit requires set_page_config to be called before any other Streamlit calls
st.set_page_config(
    page_title="Resume Builder Agent",
    page_icon="📄",
    layout="wide"
)


def main():
    # Initialize session state for storing the generated filename and data
    if 'final_filename' not in st.session_state:
        st.session_state.final_filename = None
    if 'summary_data' not in st.session_state:
        st.session_state.summary_data = None
    if 'skills_data' not in st.session_state:
        st.session_state.skills_data = None
    if 'projects_data' not in st.session_state:
        st.session_state.projects_data = None
    
    st.title("📄 Resume Builder Agent")
    st.markdown("---")
    
    # Sidebar for input
    with st.sidebar:
        st.header("📝 Job Description Input")
        st.markdown("Paste your job description below:")
        
        # Job Description input
        jd_text = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the complete job description here...",
            help="Enter the job description you want to optimize your resume for"
        )
        
        # Output filename input
        output_name_input = st.text_input(
            "Output file name (.docx)",
            value="Generated_Resume.docx",
            help="Type the file name for the generated resume"
        )
        # Sanitize and normalize to .docx (keep only basename)
        raw_name = output_name_input.strip() or "Generated_Resume.docx"
        output_name = Path(raw_name).name
        if not output_name.lower().endswith(".docx"):
            output_name = f"{output_name}.docx"
        
        # Generate button
        generate_btn = st.button("🚀 Generate Resume", type="primary", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Resume Preview")
        
        if generate_btn:
            if not jd_text.strip():
                st.error("⚠️ Please enter a job description to generate the resume.")
            else:
                with st.spinner("🔄 Generating your optimized resume..."):
                    try:
                        # Generate summary
                        st.info("📝 Generating summary...")
                        summary_data = get_llm_summary(jd_text)
                        
                        # Generate skills
                        st.info("🛠️ Optimizing skills...")
                        skills_data = get_llm_skills(jd_text)
                        
                        # Generate projects
                        st.info("💼 Processing projects...")
                        projects_data = get_llm_projects(jd_text)
                        
                        # Defensive checks for LLM outputs
                        if not summary_data or not isinstance(summary_data, dict):
                            st.error("Failed to generate summary. Try again or modify the job description.")
                            st.session_state.summary_data = None
                            st.session_state.skills_data = None
                            st.session_state.projects_data = None
                        elif not skills_data or not isinstance(skills_data, dict):
                            st.error("Failed to generate skills. Try again or modify the job description.")
                            st.session_state.summary_data = None
                            st.session_state.skills_data = None
                            st.session_state.projects_data = None
                        elif projects_data is None or not isinstance(projects_data, list):
                            st.error("Failed to generate projects. Try again or modify the job description.")
                            st.session_state.summary_data = None
                            st.session_state.skills_data = None
                            st.session_state.projects_data = None
                        elif len(projects_data) == 0:
                            st.error("No projects generated. Try again or modify the job description.")
                            st.session_state.summary_data = None
                            st.session_state.skills_data = None
                            st.session_state.projects_data = None
                        else:
                            # Store data in session state
                            st.session_state.summary_data = summary_data
                            st.session_state.skills_data = skills_data
                            st.session_state.projects_data = projects_data
                            
                            # Create resume
                            st.info("📄 Creating resume document...")
                            save_path = Path.cwd() / output_name
                            output_filename = create_resume(
                                summary_data,
                                skills_data,
                                projects_data,
                                str(save_path)
                            )

                            final_filename = output_filename or str(save_path)
                            # Convert to absolute path and ensure it exists
                            final_filename = str(Path(final_filename).resolve())
                            st.session_state.final_filename = final_filename
                            
                            # Verify file exists
                            if os.path.exists(final_filename):
                                st.success("✅ Resume generated successfully!")
                            else:
                                st.error(f"❌ Resume file not found at: {final_filename}")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating resume: {str(e)}")
                        st.exception(e)
                        st.session_state.summary_data = None
                        st.session_state.skills_data = None
                        st.session_state.projects_data = None
        
        # Display preview from session state
        if st.session_state.summary_data or st.session_state.skills_data or st.session_state.projects_data:
            st.subheader("📖 Resume Preview")
            
            # Summary preview
            if st.session_state.summary_data:
                st.write("**Summary:**")
                st.write(st.session_state.summary_data.get("summary", "No summary available"))
                
                if "subpoints" in st.session_state.summary_data and st.session_state.summary_data["subpoints"]:
                    st.write("**Key Points:**")
                    for point in st.session_state.summary_data["subpoints"]:
                        st.write(f"• {point}")
            
            # Skills preview
            if st.session_state.skills_data and "key_skills" in st.session_state.skills_data:
                st.write("**Skills:**")
                for category, skills in st.session_state.skills_data["key_skills"].items():
                    st.write(f"**{category}:** {', '.join(skills)}")
            
            # Projects preview
            if st.session_state.projects_data and isinstance(st.session_state.projects_data, list):
                st.write("**Projects:**")
                for project in st.session_state.projects_data:
                    if isinstance(project, dict):
                        st.write(f"**{project.get('title', 'Untitled Project')}**")
                        if "tech_stack" in project and project["tech_stack"] and isinstance(project["tech_stack"], list):
                            st.write(f"*Technologies: {', '.join(str(tech) for tech in project['tech_stack'])}*")
                        if "subpoints" in project and project["subpoints"] and isinstance(project["subpoints"], list):
                            for point in project["subpoints"]:
                                st.write(f"• {point}")
                        st.write("---")
    
    with col2:
        st.header("📁 Download Resume")

        # Check if a file has been generated and saved in session state
        if st.session_state.final_filename and os.path.exists(st.session_state.final_filename):
            with open(st.session_state.final_filename, "rb") as file:
                st.download_button(
                    label="📥 Download Resume",
                    data=file.read(),
                    file_name=os.path.basename(st.session_state.final_filename),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.info("👆 Generate a resume first to download it")
        
        st.markdown("---")
        st.header("ℹ️ Instructions")
        st.markdown("""
        1. **Paste Job Description**: Copy and paste the complete job description in the sidebar
        2. **Click Generate**: Press the "Generate Resume" button
        3. **Review Preview**: Check the generated content in the preview
        4. **Download**: Click the download button to get your optimized resume
        
        **Features:**
        - ✅ ATS-optimized content
        - ✅ Skills matching job requirements
        - ✅ Professional formatting
        - ✅ Ready-to-use Word document
        """)
        
        st.markdown("---")
        st.markdown("**Made with ❤️ by Resume Builder Agent**")

if __name__ == "__main__":
    main()
