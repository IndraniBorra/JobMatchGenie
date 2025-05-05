import os
import re
import datetime
import PyPDF2
import numpy as np
from flask import Blueprint, request, render_template, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy

resume_score_bp = Blueprint('resume_score', __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models
print("[INFO] Loading SentenceTransformer model...")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("[INFO] Model loaded.")

print("[INFO] Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")
print("[INFO] spaCy model loaded.")

# Extract text from PDF
def extract_text_from_pdf(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# TF-IDF similarity
def compute_similarity_from_text(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
    return score

# Embedding similarity
def compute_embedding_similarity(text1, text2):
    emb1 = embedding_model.encode(text1)
    emb2 = embedding_model.encode(text2)
    score = cosine_similarity([emb1], [emb2])[0][0]
    return score

# Skill extractor
class SkillExtractor:
    def __init__(self, text):
        self.doc = nlp(text.lower())
        self.skills = self.extract_skills()

    def extract_skills(self):
        skills = set()
        for token in self.doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                skills.add(token.lemma_)
        return skills

# Evaluation logic
def evaluate_resume_and_job(resume_text, job_desc_text):
    tfidf_score = compute_similarity_from_text(resume_text, job_desc_text)
    emb_score = compute_embedding_similarity(resume_text, job_desc_text)

    resume_skills = SkillExtractor(resume_text).skills
    jd_skills = SkillExtractor(job_desc_text).skills

    missing_skills = list(jd_skills - resume_skills)
    skill_match_pct = round(100 * (len(jd_skills & resume_skills) / len(jd_skills)), 2) if jd_skills else 0.0

    if emb_score >= 0.7:
        match_category = "Good Fit"
    elif emb_score >= 0.5:
        match_category = "Moderate Fit"
    else:
        match_category = "Poor Fit"

    return {
    "tfidf_similarity": float(round(tfidf_score, 2)),
    "embedding_similarity": float(round(emb_score, 2)),
    "skill_match_pct": float(skill_match_pct),
    "match_category": match_category,
    "missing_skills": missing_skills[:5] if missing_skills else []
    }


# Routes
@resume_score_bp.route("/resume-score")
def resume_score_page():
    return render_template("resume_score.html")

@resume_score_bp.route("/extract-text", methods=["POST"])
def extract_text_api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    text = extract_text_from_pdf(file.stream)
    return jsonify({"text": text})

@resume_score_bp.route("/compare-text", methods=["POST"])
def compare_text_api():
    data = request.get_json()
    text1 = data.get("text1", "").strip()
    text2 = data.get("text2", "").strip()
    if not text1 or not text2:
        return jsonify({"error": "Both texts are required"}), 400

    results = evaluate_resume_and_job(text1, text2)
    return jsonify(results), 200
