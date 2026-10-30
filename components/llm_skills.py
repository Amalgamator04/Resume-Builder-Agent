from llmconnections import LLMConnections
from components.geminillm import call_gemini
llm=LLMConnections()

def get_llm_skills(JD_DETAILS):
    import os
    base_dir = os.path.dirname(os.path.dirname(__file__))  # goes up from helper/
    file_path = os.path.join(base_dir, "data", "about.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        skills_data = file.read()  # Read entire file content

    base_dir = os.path.dirname(os.path.dirname(__file__))  # goes up from helper/
    file_path = os.path.join(base_dir, "data", "skills.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        resume_summary_text = file.read()  # Read entire file content

    prompt = f"""
        You are a highly analytical **ATS Optimization Specialist**. Your sole function is to construct the ideal 'Key Skills' section to achieve the highest possible Applicant Tracking System (ATS) match score for the provided candidate against the 'TARGET JOB DESCRIPTION'.

        Your process must be strictly:
        1.  **ANALYZE JD:** Identify all essential keywords, technical skills, and domain requirements from the TARGET JOB DESCRIPTION.
        2.  **SELECT:** Choose the skills from the 'CANDIDATE'S SKILLS LIST' that directly match or are highly relevant to the JD requirements.
        3.  **AUGMENT:** Add any critical, high-impact skills or technologies explicitly mentioned in the TARGET JOB DESCRIPTION that are missing from the candidate's list and don;t use negative words like passionate and determined.
        4. mention about the soft skills also mentioned in the job description and add them too

        You MUST return the output as a single JSON object with the following structure. DO NOT include any markdown ```json tags or surrounding text.
        - Not more than 4 categories in which technical languages must be there u can take that from skill list and 3-4 skills in each as per needed and some skills  needed in JOB description post.
        JSON REQUIRED OUTPUT STRUCTURE:
        {{
        "key_skills": {{
            "Category 1": ["Skill A", "Skill B", "Skill C"],
            "Category 2": ["Skill X", "Skill Y"]
        }}
        }}
    u can add skills in lists by yourself but only those skills which are there in job description so that keywords can match
        --- INPUT DATA ---

        TARGET JOB DESCRIPTION:
        {JD_DETAILS}

        CANDIDATE'S SKILLS LIST (Use this as your primary source):
        {skills_data}
        these are my starting skills, i want u to use skills which are relevant as per target job description and add some of my skills just take idea from it and some technical stuff, add keywords to increase ats score and not more than 4 skills in each category, category can be of 5-6.

        CANDIDATE'S CURRENT SUMMARY (For context only):
        {resume_summary_text}
        """

    new_skills=call_gemini(prompt=f"{prompt}")

    if new_skills is None:
        return None
    response = new_skills
    return response

