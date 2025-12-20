from flask import Flask, render_template, request, send_file, redirect, url_for
import PyPDF2
import re
from fpdf import FPDF
import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('analyses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS analyses
                 (id INTEGER PRIMARY KEY, match_percentage REAL, matched TEXT, missing TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ===============================
# SKILL CONFIGURATION
# ===============================

IMPORTANT_SKILLS = {
    "python": 3,
    "flask": 3,
    "django": 3,
    "machine": 2,
    "learning": 2,
    "ml": 2,
    "ai": 2,
    "sql": 2,
    "mysql": 2,
    "postgresql": 2,
    "aws": 3,
    "docker": 3,
    "git": 2,
    "javascript": 2,
    "html": 1,
    "css": 1,
    "react": 3,
    "nodejs": 3,
    "mongodb": 2,
    "tensorflow": 3,
    "pandas": 2,
    "numpy": 2,
    "scikit": 2,
    "pytorch": 3,
    "kubernetes": 3,
    "linux": 2,
    "bash": 2,
    "java": 2,
    "c++": 2,
    "c#": 2,
    "php": 1,
    "ruby": 2,
    "go": 3,
    "rust": 3
}

STOP_WORDS = {
    "and", "or", "with", "for", "the", "a", "an",
    "to", "in", "of", "is", "are", "as", "on"
}

GENERIC_WORDS = {
    "job", "role", "candidate", "looking", "experience",
    "years", "required", "responsibilities", "skills",
    "knowledge", "ability"
}

# ===============================
# HELPER FUNCTIONS
# ===============================

def extract_text_from_file(file, filename):
    """Safely extract text from PDF or DOCX"""
    if filename.lower().endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.lower()
    elif filename.lower().endswith('.docx'):
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.lower()
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")

def extract_keywords(text):
    """Extract clean keywords using NLP rules"""
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    return set(
        word for word in words
        if word not in STOP_WORDS
        and word not in GENERIC_WORDS
    )

def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "AI Resume Analysis Report", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Match Percentage: {result['match']}%", ln=True)
    pdf.ln(5)

    if result["matched"]:
        pdf.cell(0, 10, "Matched Skills:", ln=True)
        for skill in result["matched"]:
            pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.ln(3)

    if result["missing"]:
        pdf.cell(0, 10, "Missing Skills:", ln=True)
        for skill in result["missing"]:
            pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.output("resume_report.pdf")

@app.route('/download')
def download():
    try:
        return send_file('resume_report.pdf', as_attachment=True)
    except FileNotFoundError:
        return "Report not found. Please analyze a resume first.", 404

@app.route('/history')
def history():
    conn = sqlite3.connect('analyses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM analyses ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    analyses = []
    for row in rows:
        analyses.append({
            'id': row[0],
            'match': row[1],
            'matched': row[2].split(',') if row[2] else [],
            'missing': row[3].split(',') if row[3] else [],
            'timestamp': row[4]
        })
    return render_template('history.html', analyses=analyses)

@app.route('/clear_history')
def clear_history():
    conn = sqlite3.connect('analyses.db')
    c = conn.cursor()
    c.execute("DELETE FROM analyses")
    conn.commit()
    conn.close()
    return redirect(url_for('history'))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    job_desc = None
    error = None

    if request.method == "POST":
        resume = request.files.get("resume")
        job_desc = request.form.get("job", "").strip()

        if not resume or resume.filename == '':
            error = "Please upload a resume PDF or DOCX."
        elif not job_desc:
            error = "Please enter a job description."
        else:
            try:
                resume_text = extract_text_from_file(resume, resume.filename)
                resume_words = extract_keywords(resume_text)
                job_words = extract_keywords(job_desc.lower())

                # Only consider real technical skills
                resume_skills = {w for w in resume_words if w in IMPORTANT_SKILLS}
                job_skills = {w for w in job_words if w in IMPORTANT_SKILLS}

                matched = resume_skills & job_skills
                missing = job_skills - resume_skills

                score = 0
                total = 0

                for skill in job_skills:
                    weight = IMPORTANT_SKILLS.get(skill, 1)
                    total += weight
                    if skill in resume_skills:
                        score += weight

                match_percentage = round((score / total) * 100, 2) if total > 0 else 0

                result = {
                    "match": match_percentage,
                    "matched": sorted(list(matched)),
                    "missing": sorted(list(missing))
                }

                generate_pdf(result)

                # Save to database
                conn = sqlite3.connect('analyses.db')
                c = conn.cursor()
                c.execute("INSERT INTO analyses (match_percentage, matched, missing, timestamp) VALUES (?, ?, ?, ?)",
                          (result['match'], ','.join(result['matched']), ','.join(result['missing']), datetime.datetime.now().isoformat()))
                conn.commit()
                conn.close()
            except Exception as e:
                error = "Error processing the resume. Please ensure it's a valid PDF."

    return render_template("index.html", result=result, job_desc=job_desc, error=error)

if __name__ == "__main__":
    app.run(debug=True)
