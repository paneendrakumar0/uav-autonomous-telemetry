#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS

# Read the markdown file
with open("reports/speed_sweep_validation_2026-07-22/SPEED_SWEEP_SUMMARY.md", "r") as f:
    text = f.read()

# Extract only the observations/kinematics section
# Looking for "## Kinematic Aggressiveness" and taking the rest of the file
if "## Kinematic Aggressiveness" in text:
    observations_md = "## Kinematic Aggressiveness" + text.split("## Kinematic Aggressiveness")[1]
else:
    observations_md = text # fallback

# Provide a bit of styling
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        margin: 40px;
    }}
    h2, h3 {{
        color: #2c3e50;
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 20px;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #f2f2f2;
    }}
    code {{
        background-color: #f8f8f8;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: monospace;
    }}
    ul, ol {{
        margin-bottom: 20px;
    }}
</style>
</head>
<body>
    <h1>UAV Slung-Payload: Kinematic Observations</h1>
    {markdown.markdown(observations_md, extensions=['tables'])}
</body>
</html>
"""

# Render to PDF
pdf_path = "reports/speed_sweep_validation_2026-07-22/kinematic_observations.pdf"
HTML(string=html_content).write_pdf(pdf_path)

print(f"Successfully generated PDF: {pdf_path}")
