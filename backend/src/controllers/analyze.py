import re
import PyPDF2
import docx
from fpdf import FPDF
import datetime

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


def extract_text_from_file(file_stream, filename):
    """Extract text from PDF or DOCX file-like object and return lowercase text.

    This function is tolerant to receiving a Flask/Werkzeug FileStorage object
    or a raw file-like object. It will attempt to detect the file type by
    filename first, then fall back to inspecting the file header bytes.
    """
    # If this is a Werkzeug FileStorage, use its stream
    stream = getattr(file_stream, 'stream', file_stream)

    # Ensure we can read header bytes for type detection
    try:
        pos = stream.tell() if hasattr(stream, 'tell') else None
    except Exception:
        pos = None

    header = b''
    try:
        header = stream.read(8)
    except Exception:
        header = b''

    # Reset stream position if possible
    try:
        if pos is not None:
            stream.seek(pos)
        else:
            stream.seek(0)
    except Exception:
        pass

    fname = (filename or '').lower()
    is_pdf = fname.endswith('.pdf') or header.startswith(b'%PDF')
    is_docx = fname.endswith('.docx') or header.startswith(b'PK')

    if is_pdf:
        reader = PyPDF2.PdfReader(stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.lower()
    elif is_docx:
        # docx expects a path or a file-like object positioned at start
        try:
            # ensure stream is at start
            try:
                stream.seek(0)
            except Exception:
                pass
            doc = docx.Document(stream)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text.lower()
        except Exception:
            raise ValueError("Could not parse DOCX file. Ensure the file is a valid .docx archive.")
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")


SKILL_SYNONYMS = {
    'c++': ['c++', 'cplusplus'],
    'c#': ['c#', 'csharp'],
    'nodejs': ['node', 'nodejs', 'node.js'],
    'tensorflow': ['tensorflow', 'tf'],
    'scikit': ['scikit', 'scikit-learn', 'sklearn'],
    'postgresql': ['postgres', 'postgresql'],
}


def _normalize_token(tok: str) -> str:
    t = tok.lower().strip()
    # normalize common punctuation
    t = t.replace('node.js', 'nodejs')
    t = t.replace('csharp', 'c#')
    t = t.replace('cplusplus', 'c++')
    t = t.replace('sklearn', 'scikit')
    t = t.replace('tf', 'tensorflow')
    # remove trailing non-alphanum except + and #
    t = re.sub(r"^[^a-z0-9#+]+|[^a-z0-9#+]+$", "", t)
    return t


def extract_keywords(text):
    # allow letters, numbers, +, #, dots and hyphens inside tokens
    words = re.findall(r"[A-Za-z0-9#+\.\-]{1,}", text)
    cleaned = set()
    for word in words:
        w = _normalize_token(word)
        if not w:
            continue
        if w in STOP_WORDS or w in GENERIC_WORDS:
            continue
        # map synonyms to canonical skill name
        mapped = w
        for canon, variants in SKILL_SYNONYMS.items():
            if w in variants or w == canon:
                mapped = canon
                break
        cleaned.add(mapped)
    return cleaned


def compute_match_and_result(resume_text, job_text):
    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_text)

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
    return result


def generate_pdf(result, out_path="resume_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "AI Resume Analysis Report", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Match Percentage: {result['match']}%", ln=True)
    pdf.ln(5)

    if result.get("matched"):
        pdf.cell(0, 10, "Matched Skills:", ln=True)
        for skill in result.get("matched", []):
            pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.ln(3)

    if result.get("missing"):
        pdf.cell(0, 10, "Missing Skills:", ln=True)
        for skill in result.get("missing", []):
            pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.output(out_path)
