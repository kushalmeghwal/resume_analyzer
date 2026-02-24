def generate_markdown_report(data: dict, filename="resume_report.md"):
    """Generate markdown report from analysis."""
    
    report = f"""
# Resume Analysis Report

## Match Score
{data['score']}%

## Matching Skills
{", ".join(data['matched'])}

## Missing Keywords
{", ".join(data['missing'])}

## Suggestions
{data['suggestions']}
"""

    with open(filename, "w") as f:
        f.write(report)

    return filename