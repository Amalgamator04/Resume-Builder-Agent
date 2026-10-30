
from llmconnections import LLMConnections
from components.geminillm import call_gemini
llm=LLMConnections()

def get_llm_summary(JD_DETAILS):
# Open the file in read mode
    import os
    base_dir = os.path.dirname(os.path.dirname(__file__))  # goes up from helper/
    file_path = os.path.join(base_dir, "data", "about.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        text_data = file.read()  # Read entire file content

    prompt=f"""Your response must be strictly in JSON format, containing only two keys: "summary" and "subpoints".  
The required JSON structure is as follows:


  "summary": "Your new, ATS-optimized summary text goes here.",
  "subpoints": [
    "First job-focused bullet point goes here.",
    "Second job-focused bullet point goes here.",
    "Third job-focused bullet point goes here."
  ]


ABOUT:
{text_data}

The "summary" should be written based on the information provided in ABOUT but should primarily focus on the JOB_DESCRIPTION and its requirements.  
Do not copy the ABOUT section directly — instead, use it to understand my background and tailor the summary to emphasize the skills, experience, and qualities relevant to the job description.  

JOB_DESCRIPTION:
{JD_DETAILS}

Guidelines:
- Keep the response concise, professional, and ATS-friendly.
- Make sure to add my details and tune it according to JOB DESCRIPTION
- Include no more than three subpoints.
- Total words of response must be of 90 words only not greater than 90 words.
-Total words of response must be of 90 words only not greater than 90 words
- Ensure the JSON syntax is valid and properly formatted.
- Add Company name if it's there.
- Also mention about the Job Description post in summary.
- Mention about the Degree mentioned in the JD, I have done B.tech in CSE so do mention Bachlor of Technology in Computer Science and Engineering.
- you're confident you can perform the job and meet other criteria, consider applying. Include a strong summary explaining why you're a great fit despite having fewer years of experience. Be aware that experience is often an initial screening factor.
"""

    new_summary=call_gemini(prompt=f"{prompt}")
    
    if new_summary is None:
        raise ValueError("LLM did not return a response.")
    response=new_summary
    
    return response


