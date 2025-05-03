from flask import Flask, render_template
from resume_score import resume_score_bp
from resume_parser import resume_parser_bp
from cover_letter import cover_letter_bp 

app = Flask(__name__)
app.register_blueprint(resume_score_bp)
app.register_blueprint(resume_parser_bp)
app.register_blueprint(cover_letter_bp)  

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)