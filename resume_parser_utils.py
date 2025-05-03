# resume_parser_utils.py

import re
from pdfminer.high_level import extract_text

def extract_text_from_pdf_stream(pdf_stream):
    return extract_text(pdf_stream)

def extract_contact_number(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_email(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_skills(text, skills_list):
    found_skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

def parse_resume(pdf_stream):
    text = extract_text_from_pdf_stream(pdf_stream)

    skills_list = [
        'Python', 'Data Analysis', 'Machine Learning', 'Communication',
        'Project Management', 'Deep Learning', 'SQL', 'Tableau',
        'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular'
    ]

    return {
        "email": extract_email(text),
        "phone": extract_contact_number(text),
        "skills": extract_skills(text, skills_list),
        "text_preview": text[:1000]  # Optional: preview of raw text
    }
