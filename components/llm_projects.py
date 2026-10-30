import os

from components.geminillm import call_gemini


def get_llm_projects(JD_DETAILS):

    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "skills.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        skills_data = file.read()

    file_path = os.path.join(base_dir, "data", "projects.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        projects_data = file.read()

    prompt = f"""
You are an ATS Optimization and Resume Intelligence Specialist.
Your goal is to construct a highly optimized "Projects" section that maximizes the Applicant Tracking System (ATS) match score for the candidate, aligning their profile precisely with the TARGET JOB DESCRIPTION.

Analyze the given TARGET JOB DESCRIPTION, CANDIDATE SKILLS LIST, and PROJECTS to produce a JSON output that follows the structure and rules below.

INSTRUCTIONS:

1. ANALYZE JD:
   -Identify all essential keywords, technical tools, and domain-specific skills from the TARGET JOB DESCRIPTION.
   -Out of so many projects choose project close to the JOB DESCRIPTION and reframe the subpoints as per JD needs and requirements.

2. ALIGN, SELECT, REFRAME & OPTIMIZE:
   From the provided project data, generate exactly three project entries that align most closely with the target job post needs.
   Each project must:
   - Be reframed to highlight the skills and technologies that directly match the JD requirements.
   - Include a concise, domain-relevant title.
   - Include a tech_stack list of exactly three relevant technologies or tools.
   - Have three bullet points describing:
     1. The project purpose or goal using action-oriented and keyword-rich language.
     2. Your technical contributions or methods, emphasizing how the candidate's skills and specific tools were applied in context of JD requirements.
     3. Quantifiable results or measurable outcomes demonstrating impact on performance, users, or efficiency (use metrics or numbers where possible).
   Focus on ATS-relevant keywords, industry terminology, and JD alignment. Avoid hallucination; ensure all details are contextually accurate, concise, and optimized for keyword scanning by Applicant Tracking Systems aligned with JD needs.

3. OUTPUT FORMAT:
   - Return only valid JSON (no markdown, code blocks, or text outside JSON).
   - Do not include explanations, prefaces, or summaries.
   - Make sure to add atleast two times the keyword u thing is relevant from JD in each subpoint to increase ATS score.
   - Don't add anything by yourself only use the given information and frame it


REQUIRED JSON OUTPUT STRUCTURE:
{{
  "projects": [
    {{
      "title": "Project Title 1",
      "tech_stack": ["Technology 1", "Technology 2", "Technology 3"],
      "subpoints": [
        "Point 1 describing the project purpose.",
        "Point 2 explaining technical contribution.",
        "Point 3 summarizing quantifiable results."
      ]
    }},
    {{
      "title": "Project Title 2",
      "tech_stack": ["Technology 1", "Technology 2", "Technology 3"],
      "subpoints": [
        "Point 1 describing the project purpose.",
        "Point 2 explaining technical contribution.",
        "Point 3 summarizing quantifiable results."
      ]
    }},
    {{
      "title": "Project Title 3",
      "tech_stack": ["Technology 1", "Technology 2", "Technology 3"],
      "subpoints": [
        "Point 1 describing the project purpose.",
        "Point 2 explaining technical contribution.",
        "Point 3 summarizing quantifiable results."
      ]
    }}
  ]
}}

INPUT DATA:

TARGET JOB DESCRIPTION:
{JD_DETAILS}

CANDIDATE SKILLS LIST:
{skills_data}

PROJECTS:
{projects_data}
"""

    response = call_gemini(prompt=prompt)

    if response is None:
        raise ValueError("LLM did not return a response.")

    if isinstance(response, dict) and "projects" in response:
        return response["projects"]

    return response if isinstance(response, list) else []

