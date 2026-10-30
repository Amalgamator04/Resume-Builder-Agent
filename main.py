
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from components.llm_summary import get_llm_summary
from components.llm_skills import get_llm_skills
from components.llm_projects import get_llm_projects


def add_hyperlink(paragraph, url, text):
    """
    A function that places a hyperlink within a paragraph object.
    """
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    
    # Create text element with proper formatting
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Calibri')
    rFonts.set(qn('w:hAnsi'), 'Calibri')
    rPr.append(rFonts)
    
    # Add color (blue) and underline to text properties
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0563C1')
    rPr.append(color)
    
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    
    new_run.append(rPr)
    
    # Create the text element
    t = OxmlElement('w:t')
    t.text = text
    new_run.append(t)
    
    hyperlink.append(new_run)
    paragraph._element.append(hyperlink)
    
    return hyperlink


def create_resume(summary_data, skills_data, projects_data, output_filename="Prabhav_Sharma_Resume.docx"):
    """
    Creates a resume document with the same structure as your original resume.
    
    Args:
        summary_data: Dict with 'summary' and 'subpoints' keys
            Example: {
                "summary": "Your summary text here.",
                "subpoints": ["Point 1", "Point 2", "Point 3"]
            }
        
        skills_data: Dict with 'key_skills' containing categories and skills list
            Example: {
                'key_skills': {
                    'Category 1': ['Skill A', 'Skill B', 'Skill C'],
                    'Category 2': ['Skill X', 'Skill Y']
                }
            }
        
        projects_data: List of dicts, each with 'title', 'tech_stack', and 'subpoints'
            Example: [
                {
                    "title": "Project Title 1",
                    "tech_stack": ["Technology 1", "Technology 2"],
                    "subpoints": ["Point 1", "Point 2", "Point 3"]
                }
            ]
        
        output_filename: Name of the output file (default: "Prabhav_Sharma_Resume.docx")
    """
    doc = Document()
    
    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.3)
        section.bottom_margin = Inches(0.3)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
    
    # ==================== HEADER SECTION (STATIC) ====================
    # Name - Centered at top
    name_para = doc.add_paragraph()
    name_run = name_para.add_run("Prabhav Sharma")
    name_run.bold = True
    name_run.font.size = Pt(16)
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_para.paragraph_format.space_after = Pt(0)
    
    # All contact info in a single line - Centered
    contact_para = doc.add_paragraph()
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_para.paragraph_format.space_after = Pt(6)
    
    contact_run = contact_para.add_run("Delhi, New Delhi-12 | +91-7303025805 | ")
    contact_run.font.size = Pt(10)
    
    # Email link
    add_hyperlink(contact_para, "mailto:prabhavs2004@gmail.com", "prabhavs2004@gmail.com")
    contact_para.add_run(" | ").font.size = Pt(10)
    
    # GitHub link
    add_hyperlink(contact_para, "https://github.com/Amalgamator04", "GitHub")
    contact_para.add_run(" | ").font.size = Pt(10)
    
    # Portfolio link
    add_hyperlink(contact_para, "https://prabhavportfolio.netlify.app/", "Portfolio")
    contact_para.add_run(" | ").font.size = Pt(10)
    
    # LinkedIn link
    add_hyperlink(contact_para, "https://www.linkedin.com/in/prabhav-sharma-6b3ba8263/", "LinkedIn")
    
    # ==================== SUMMARY SECTION (DYNAMIC) ====================
    summary_heading = doc.add_paragraph()
    summary_heading_run = summary_heading.add_run("Summary")
    summary_heading_run.bold = True
    summary_heading_run.font.size = Pt(14)
    summary_heading_run.font.color.rgb = RGBColor(0, 0, 0)  # Black
    summary_heading.paragraph_format.space_after = Pt(0)
    
    # Main summary paragraph
    summary_para = doc.add_paragraph(summary_data["summary"])
    summary_para.paragraph_format.space_after = Pt(0)
    for run in summary_para.runs:
        run.font.size = Pt(11)
    
    # Summary subpoints (if provided)
    if "subpoints" in summary_data and summary_data["subpoints"]:
        for subpoint in summary_data["subpoints"]:
            subpoint_para = doc.add_paragraph(subpoint, style='List Bullet')
            subpoint_para.paragraph_format.left_indent = Inches(0.25)
            subpoint_para.paragraph_format.space_after = Pt(0)
            for run in subpoint_para.runs:
                run.font.size = Pt(11)
    
    # ==================== SKILLS SECTION (DYNAMIC) ====================
    skills_heading = doc.add_paragraph()
    skills_heading_run = skills_heading.add_run("Skills")
    skills_heading_run.bold = True
    skills_heading_run.font.size = Pt(14)
    skills_heading_run.font.color.rgb = RGBColor(0, 0, 0)  # Black
    skills_heading.paragraph_format.space_before = Pt(2)
    skills_heading.paragraph_format.space_after = Pt(0)
    
    # Extract key_skills from the nested structure
    key_skills = skills_data.get('key_skills', {})
    
    for category, skills_list in key_skills.items():
        skills_para = doc.add_paragraph()
        
        # Category name (bold)
        category_run = skills_para.add_run(f"• {category}: ")
        category_run.bold = True
        category_run.font.size = Pt(11)
        
        # Skills list
        skills_text = ", ".join(skills_list)
        skills_run = skills_para.add_run(skills_text)
        skills_run.font.size = Pt(11)
        skills_para.paragraph_format.space_after = Pt(0)
    
    # ==================== PROJECTS SECTION (DYNAMIC) ====================
    projects_heading = doc.add_paragraph()
    projects_heading_run = projects_heading.add_run("Work Experience")
    projects_heading_run.bold = True
    projects_heading_run.font.size = Pt(14)
    projects_heading_run.font.color.rgb = RGBColor(0, 0, 0)  # Black
    projects_heading.paragraph_format.space_before = Pt(2)
    projects_heading.paragraph_format.space_after = Pt(0)
    
    for i, project in enumerate(projects_data):
        # Project title and tech stack
        project_title_para = doc.add_paragraph()
        
        # Title (bold)
        title = project.get("title", "Untitled Project")
        title_run = project_title_para.add_run(title)
        title_run.bold = True
        title_run.font.size = Pt(11)
        
        # Tech stack (italic, in square brackets)
        tech_stack = project.get("tech_stack", [])
        if tech_stack and isinstance(tech_stack, list):
            tech_stack_text = f" [{', '.join(str(tech) for tech in tech_stack)}]"
            tech_run = project_title_para.add_run(tech_stack_text)
            tech_run.italic = True
            tech_run.font.size = Pt(11)
        project_title_para.paragraph_format.space_after = Pt(0)
        
        # Project subpoints
        subpoints = project.get("subpoints", [])
        if subpoints and isinstance(subpoints, list):
            for subpoint in subpoints:
                subpoint_para = doc.add_paragraph(str(subpoint), style='List Bullet')
                subpoint_para.paragraph_format.left_indent = Inches(0.25)
                subpoint_para.paragraph_format.space_after = Pt(0)
                for run in subpoint_para.runs:
                    run.font.size = Pt(11)
        
        # Add separator line between projects (except after last project)
        # if i < len(projects_data) - 1:
        #     separator_para = doc.add_paragraph()
        #     separator_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #     separator_run = separator_para.add_run("_" * 80)
        #     separator_run.font.size = Pt(8)
        #     separator_para.paragraph_format.space_before = Pt(4)
        #     separator_para.paragraph_format.space_after = Pt(4)
    
    # ==================== EDUCATION SECTION (STATIC) ====================
    education_heading = doc.add_paragraph()
    education_heading_run = education_heading.add_run("Education")
    education_heading_run.bold = True
    education_heading_run.font.size = Pt(14)
    education_heading_run.font.color.rgb = RGBColor(0, 0, 0)  # Black
    education_heading.paragraph_format.space_before = Pt(6)
    education_heading.paragraph_format.space_after = Pt(0)
    
    edu1 = doc.add_paragraph("PCM 12th | Gyan Mandir Public School| New Delhi | 2020-22", style='List Bullet')
    edu1.paragraph_format.left_indent = Inches(0.25)
    edu1.paragraph_format.space_after = Pt(0)
    for run in edu1.runs:
        run.font.size = Pt(11)
    
    edu2 = doc.add_paragraph("B.Tech (CSE) | Jims Mangement Technical Campus, Greater Noida | 2022-26", style='List Bullet')
    edu2.paragraph_format.left_indent = Inches(0.25)
    edu2.paragraph_format.space_after = Pt(0)
    for run in edu2.runs:
        run.font.size = Pt(11)
    
    # ==================== INTERNSHIP & TRAINING SECTION (STATIC) ====================
    internship_heading = doc.add_paragraph()
    internship_heading_run = internship_heading.add_run("Internship & Training")
    internship_heading_run.bold = True
    internship_heading_run.font.size = Pt(14)
    internship_heading_run.font.color.rgb = RGBColor(0, 0, 0)  # Black
    internship_heading.paragraph_format.space_before = Pt(6)
    internship_heading.paragraph_format.space_after = Pt(0)
    
    int1 = doc.add_paragraph("Data Analyst Intern in Bharti Airtel (April 2025 – June 2025)", style='List Bullet')
    int1.paragraph_format.left_indent = Inches(0.25)
    int1.paragraph_format.space_after = Pt(0)
    for run in int1.runs:
        run.font.size = Pt(11)
    
    int2 = doc.add_paragraph("Data Science & Machine Learning (Udemy)", style='List Bullet')
    int2.paragraph_format.left_indent = Inches(0.25)
    int2.paragraph_format.space_after = Pt(0)
    for run in int2.runs:
        run.font.size = Pt(11)
    
    
    # Save the document
    doc.save(output_filename)
    print(f"Resume created successfully: {output_filename}")
    return output_filename


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    from components.variable import JD
    JD_DETAILS = JD
    # Generate data by calling functions directly
    print("Generating summary...")
    summary_data = get_llm_summary(JD_DETAILS)
    
    print("Generating skills...")
    skills_data = get_llm_skills(JD_DETAILS)
    
    print("Generating projects...")
    projects_data = get_llm_projects(JD_DETAILS)
    
    # Create the resume
    create_resume(summary_data, skills_data, projects_data, "Prabhav_Sharma_Resume.docx")