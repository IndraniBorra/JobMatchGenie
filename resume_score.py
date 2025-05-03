# resume_score.py

import os
import PyPDF2
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create Blueprint
resume_score_bp = Blueprint('resume_score', __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ────────────────────────────────────────────────
# Utility Functions
# ────────────────────────────────────────────────

def extract_text_from_pdf(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def compute_similarity_from_text(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
    return score

def compute_similarity_from_pdfs(pdf1_stream, pdf2_stream):
    text1 = extract_text_from_pdf(pdf1_stream)
    text2 = extract_text_from_pdf(pdf2_stream)
    return compute_similarity_from_text(text1, text2)

# ────────────────────────────────────────────────
# Page Route
# ────────────────────────────────────────────────

@resume_score_bp.route("/resume-score")
def resume_score_page():
    return render_template("resume_score.html")

# ────────────────────────────────────────────────
# Compare PDFs (old API)
# ────────────────────────────────────────────────

@resume_score_bp.route("/compare", methods=["POST"])
def compare_pdfs():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Please upload two files: file1 and file2"}), 400

    f1 = request.files['file1']
    f2 = request.files['file2']

    try:
        score = compute_similarity_from_pdfs(f1.stream, f2.stream)
        return jsonify({"similarity": score}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ────────────────────────────────────────────────
# Extract text from one PDF (AJAX support)
# ────────────────────────────────────────────────

@resume_score_bp.route("/extract-text", methods=["POST"])
def extract_text_api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    text = extract_text_from_pdf(file.stream)
    return jsonify({"text": text})

# ────────────────────────────────────────────────
# Compare pasted text input
# ────────────────────────────────────────────────

@resume_score_bp.route("/compare-text", methods=["POST"])
def compare_text_api():
    data = request.get_json()
    text1 = data.get("text1", "").strip()
    text2 = data.get("text2", "").strip()
    if not text1 or not text2:
        return jsonify({"error": "Both texts are required"}), 400
    try:
        score = compute_similarity_from_text(text1, text2)
        return jsonify({"similarity": score}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
