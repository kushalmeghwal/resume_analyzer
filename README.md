# Smart Resume Analyzer (Google ADK)

A multi-agent resume analyzer that compares a resume PDF with a target job description, identifies skill gaps, suggests improvements, and generates a markdown report.

## Tech Stack
- Python 3.10+ (recommended: 3.11)
- Google ADK
- Gemini stable model (`gemini-1.5-flash`)
- `python-dotenv`
- `pdfplumber` / `pypdf`

## Project Structure

```text
resume_analyzer/
├── agent.py
├── sub_agents/
│   ├── extractor_agent.py
│   ├── keyword_agent.py
│   ├── improvement_agent.py
│   └── report_agent.py
├── tools/
│   ├── pdf_tool.py
│   ├── keyword_tool.py
│   └── report_tool.py
├── sample_data/
│   ├── resume.pdf
│   └── job_description.txt
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── problem_statement.md
```

## Setup

### 1) Create venv
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3) Configure environment
Create `.env`:

```env
GOOGLE_API_KEY=your_key_here
```

## How It Works (Sequential Multi-Agent Workflow)
1. `ResumeExtractionAgent` reads the PDF via `extract_pdf_text(filepath)`.
2. `KeywordAnalysisAgent` compares resume text and JD via `analyze_keywords(resume_text, job_description)`.
3. `ImprovementSuggestionAgent` uses Gemini (or fallback logic) to suggest improvements.
4. `ReportGeneratorAgent` writes `resume_report.md` via `generate_markdown_report(data)`.

Root orchestration is in `agent.py`.

## Run (Local CLI)

```bash
python agent.py \
  --resume sample_data/resume.pdf \
  --job sample_data/job_description.txt \
  --out resume_report.md
```

## Run with ADK
From the parent directory of this project:

```bash
adk run resume_analyzer
adk web
```

## Required Tools Implemented
- `extract_pdf_text(filepath)`
- `analyze_keywords(resume_text, job_description)`
- `generate_markdown_report(data)`
- ADK built-in tool in root agent: `google_search`

## Sample Input
Job Description example (`sample_data/job_description.txt`):
- Python
- FastAPI/Django
- REST APIs
- PostgreSQL
- Docker
- AWS
- CI/CD
- Unit testing
- Microservices

## Sample Output (`resume_report.md`)

```md
# Resume Analysis Report

## Match Score
78%

## Matching Skills
- Python
- FastAPI
- REST APIs
- PostgreSQL

## Missing Keywords
- Docker
- AWS
- CI/CD
- Microservices

## Suggested Improvements
- Add hands-on experience with Docker and containerized deployments
- Mention cloud projects on AWS (EC2, Lambda, or S3)
- Use action verbs like "Designed", "Implemented", and "Optimized"

## Summary
Your resume is strong for Python backend roles but can improve cloud and DevOps alignment.
```
