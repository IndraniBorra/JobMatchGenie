import os
from flask import Blueprint, render_template, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
import PyPDF2

cover_letter_bp = Blueprint("cover_letter", __name__)

# Load fine-tuned model
model_path = "models/t5_cover_letter_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Utility: Extract text from PDF stream
def extract_text_from_pdf(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# Core Cover Letter Generator
def generate_cover_letter(resume_text, jd_text, tone="professional"):
    if tone == "academic":
        prompt = (
            "You are a university career counselor crafting a formal, academic-style cover letter.\n\n"
            f"Job Description: {jd_text}\n\n"
            f"Candidate Resume: {resume_text}\n\n"
            "Write a formal cover letter highlighting the candidate's educational background, research experience, and enthusiasm for continuous learning."
        )
    elif tone == "experienced":
        prompt = (
            "You are a senior career advisor writing a cover letter for an experienced computer science professional.\n\n"
            f"Job Description: {jd_text}\n\n"
            f"Candidate Resume: {resume_text}\n\n"
            "Write a confident cover letter emphasizing the candidate's industry experience, leadership, and technical expertise."
        )
    elif tone == "talented":
        prompt = (
            "You are a career mentor writing a cover letter for a talented and ambitious computer science candidate.\n\n"
            f"Job Description: {jd_text}\n\n"
            f"Candidate Resume: {resume_text}\n\n"
            "Write a passionate and inspiring cover letter showcasing the candidate's skills, innovative mindset, and eagerness to grow."
        )
    elif tone == "confident":
        prompt = (
            "You are an expert cover letter writer specializing in confident and impactful letters.\n\n"
            f"Job Description: {jd_text}\n\n"
            f"Candidate Resume: {resume_text}\n\n"
            "Write a bold, confident cover letter emphasizing the candidate's achievements and why they are the ideal fit."
        )
    else:  # fallback: professional
        prompt = (
            "You are a professional career coach writing a personalized, engaging cover letter.\n\n"
            f"Job Description: {jd_text}\n\n"
            f"Candidate Resume: {resume_text}\n\n"
            "Write a unique and compelling cover letter highlighting the candidate's fit for this role."
        )

    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True, padding="max_length", max_length=512).input_ids
    generated_ids = model.generate(
        input_ids,
        max_length=512,
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
        top_k=50,
        num_return_sequences=1,
    )
    return tokenizer.decode(generated_ids[0], skip_special_tokens=True)

# Main route: /cover-letter
@cover_letter_bp.route("/cover-letter", methods=["GET", "POST"])
def cover_letter_page():
    result = None
    if request.method == "POST":
        resume_text = request.form.get("resume", "")
        jd_text = request.form.get("jd", "")
        tone = request.form.get("tone", "professional")

        if not resume_text or not jd_text:
            result = "Both resume and job description are required."
        else:
            result = generate_cover_letter(resume_text, jd_text, tone)

    return render_template("cover_letter.html", result=result)

# AJAX route: /cover-letter/extract-text
@cover_letter_bp.route("/cover-letter/extract-text", methods=["POST"])
def extract_text_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    try:
        text = extract_text_from_pdf(file.stream)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
