def analyze_keywords(resume_text: str, job_description: str):
    """Compare resume text with job description keywords."""
    
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    matched = resume_words.intersection(job_words)
    missing = job_words.difference(resume_words)

    return {
        "matched": list(matched),
        "missing": list(missing)
    }