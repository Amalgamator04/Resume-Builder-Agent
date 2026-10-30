from llm_projects import get_llm_projects

if __name__ == "__main__":
    jd = "Python developer with AI, FastAPI, SQL, and machine learning"
    result = get_llm_projects(jd)
    print(type(result))
    print(result)
