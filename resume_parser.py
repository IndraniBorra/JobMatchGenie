from flask import Blueprint, request, render_template, jsonify
from resume_parser_utils import parse_resume

resume_parser_bp = Blueprint('resume_parser', __name__)

@resume_parser_bp.route("/resume-parser")
def resume_parser_form():
    return render_template("resume_parser.html")

@resume_parser_bp.route("/parse-resume", methods=["POST"])
def parse_resume_api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    result = parse_resume(file.stream)
    return jsonify(result)
