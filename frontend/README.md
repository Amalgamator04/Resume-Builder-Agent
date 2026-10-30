Frontend for Resume Builder Agent

Files:
- `index.html` — single-page UI for job description input, filename, generate and download.
- `styles.css` — lightweight styles used by the page.
- `app.js` — client logic that POSTs to `/api/generate` and downloads from `/api/download`.

Expected backend API (you can implement these in Flask, FastAPI, or Streamlit endpoints):

1) POST /api/generate
   - Request JSON: { "job_description": "...", "output_file": "Generated_Resume.docx" }
   - Response JSON (200):
     {
       "summary": { "summary": "...", "subpoints": ["...", "..."] },
       "skills": { "key_skills": { "Category": ["skill1","skill2"] } },
       "projects": [ {"title":"...","tech_stack":["..."],"subpoints":["..."]} ... ],
       "file_id": "<id-or-filename-to-download>"
     }
   - Notes: `file_id` should be something the download endpoint can use (filename or uuid).

2) GET /api/download?file_id=<id>
   - Returns the .docx binary with appropriate headers (Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document and Content-Disposition with filename).

3) Optional: GET /api/ping
   - Simple health-check that returns 200 OK.

Integration suggestions:
- You can implement a thin Flask app that imports your existing `create_resume` function and the components to generate the content. On `POST /api/generate` call the same flow you have in `application.py`, save the file to a temporary folder, and return `file_id` as the saved filename. On `GET /api/download` stream the saved file.

Security and deployment notes:
- Sanitize and restrict where the backend writes files to avoid arbitrary file overwrite.
- If deployed publicly, add rate-limits and authentication for LLM requests.

Next steps I can take for you:
- Implement the minimal Flask backend that uses your existing Python functions and serves the two endpoints described above.
- Or adapt the frontend to call your Streamlit app (less straightforward), or bundle everything into a single Flask+frontend app.

Tell me which integration you'd like and I'll implement it.