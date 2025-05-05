# 🧠 NLP Resume Assistant – Quick Start

This web application provides three main features:
- ✅ Resume Parsing & Job Category Prediction  
- 📊 Resume & JD Match Scoring  
- ✍️ AI-based Cover Letter Generation  

---

## 🔧 How to Run This Project

### 1. Clone the Repository
```bash
git clone https://github.com/Abhiram0908/nlp-resume-assistant.git
cd nlp-resume-assistant
```

### 2. Create and Activate a Virtual Environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```

Then open your browser and go to:  
👉 http://127.0.0.1:5000

---

## 📁 Project Structure

```
├── app.py                      # Flask main entry point
├── cover_letter.py            # Cover letter generation logic
├── resume_parser.py           # Resume parsing + category classification
├── resume_parser_utils.py     # Helper functions for parsing
├── resume_score.py            # Resume vs JD matching logic
├── requirements.txt           # Project dependencies
├── README.md                  # This file
│
├── models/                    # Trained models (T5, classifiers, vectorizers)
├── task_notebooks/            # Jupyter notebooks used for training models
├── templates/                 # HTML templates for the web app
├── static/                    # CSS/JS styles and assets
├── Proposal.pdf               # Initial project proposal
```

---

## 📽️ Demo Video

Watch the project walkthrough here:  
👉 https://youtu.be/w94-_X9GRA8?si=r7sI4KM4ZtCCOYZq