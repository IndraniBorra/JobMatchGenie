from flask import Blueprint, render_template, request
from transformers import T5ForConditionalGeneration, T5Tokenizer

cover_letter_bp = Blueprint("cover_letter", __name__)

# Load model and tokenizer once when blueprint is loaded
MODEL_PATH = "models/t5_cover_letter_model"
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

@cover_letter_bp.route("/cover-letter", methods=["GET", "POST"])
def generate_cover_letter():
    generated_letter = None

    if request.method == "POST":
        resume = request.form.get("resume", "")
        jd = request.form.get("jd", "")

        if resume.strip() and jd.strip():
            prompt = f"generate cover letter: Resume: {resume} Job: {jd}"
            inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
            outputs = model.generate(**inputs, max_new_tokens=400)
            generated_letter = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return render_template("cover_letter.html", result=generated_letter)
