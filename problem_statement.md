# Problem Statement

## Problem Definition
Resume screening is often manual, inconsistent, and slow. Candidates also struggle to understand why their resume does not align with a specific role.

## Why This Is Useful
A smart analyzer can:
- quickly compare resumes against role-specific requirements,
- expose missing keywords/skills,
- suggest targeted improvements,
- produce a reusable, structured report for iteration.

## System Workflow
1. User provides a resume PDF path and job description.
2. Resume Extraction Agent extracts text from PDF.
3. Keyword Analysis Agent identifies matching and missing skills.
4. Improvement Suggestion Agent generates actionable recommendations.
5. Report Generator Agent saves a markdown report (`resume_report.md`).

This gives both recruiters and candidates a fast, transparent fit analysis for Python-oriented backend roles.
