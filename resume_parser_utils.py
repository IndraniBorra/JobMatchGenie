import re
import io
from pdfminer.high_level import extract_text

import os
import pickle

resume_model_path = os.path.join("models", "resume_model")

with open(os.path.join(resume_model_path, "rf_classifier_categorization.pkl"), "rb") as f:
    categorizer = pickle.load(f)

with open(os.path.join(resume_model_path, "tfidf_vectorizer_categorization.pkl"), "rb") as f:
    tfidf_cat = pickle.load(f)

with open(os.path.join(resume_model_path, "rf_classifier_job_recommendation.pkl"), "rb") as f:
    recommender = pickle.load(f)

with open(os.path.join(resume_model_path, "tfidf_vectorizer_job_recommendation.pkl"), "rb") as f:
    tfidf_recom = pickle.load(f)

def predict_resume_category(text):
    vector = tfidf_cat.transform([text])
    prediction = categorizer.predict(vector)
    return prediction[0]

def recommend_jobs(text):
    vector = tfidf_recom.transform([text])
    prediction = recommender.predict(vector)
    return prediction[0]


def extract_text_from_pdf_stream(pdf_stream):
    # Read file into memory and wrap in BytesIO to ensure compatibility
    file_stream = io.BytesIO(pdf_stream.read())
    file_stream.seek(0)
    return extract_text(file_stream)

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
        "category": predict_resume_category(text),
        "job_recommendation": recommend_jobs(text),
        "email": extract_email(text),
        "phone": extract_contact_number(text),
        "skills": extract_skills(text, skills_list),
        "text_preview": text[:50000]  
    }