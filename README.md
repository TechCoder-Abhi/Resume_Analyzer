# Resume Analyzer

Resume Analyzer is a lightweight Flask web application that evaluates candidate resumes against job descriptions. It extracts skills and relevant keywords from a candidate's resume and compares them to the target job description to produce a compatibility score, lists of matched and missing skills, and an optional downloadable PDF report.

## Key Features

- Multi-format resume upload: PDF and DOCX
- Keyword extraction and normalized matching
- Match score and detailed matched/missing skills lists
- Downloadable analysis report (PDF)
- Analysis history persisted in SQLite with options to view, delete, or clear
- Simple, responsive Jinja2-based UI with dashboard and insights pages

## Architecture & Flow

1. Client posts a resume file and a job description to the `/` route via the web UI.
2. Server receives the file (`FileStorage`) and extracts text using PDF/DOCX parsers.
3. Text is normalized and tokenized; keywords are extracted and weighted.
4. The system compares job description keywords to resume keywords and computes a match percentage and lists of matched and missing skills.
5. Results are persisted to the SQLite database and rendered on the results page; a PDF report can be generated and downloaded.

High-level layout:

- `app.py` — application launcher (imports and runs `backend.run`)
- `backend/` — Flask application package (factory, routes, controllers, db helpers)
- `frontend/` — Jinja templates and static assets (CSS/JS)
- `backend/data/analyses.db` — default location for runtime SQLite DB (ignored by git)

## Environment & Configuration

- Python 3.10+ recommended.
- Key environment variables:
  - `ANALYSES_DB` — optional path to the SQLite DB file (overrides default `backend/data/analyses.db`).
  - `FLASK_ENV` — set to `development` for debug mode.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/TechCoder-Abhi/Resume_Analyzer.git
cd AI-Resume-Analyzer
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) Install the spaCy model used by NLP components:

```bash
python -m spacy download en_core_web_sm
```

5. Start the app:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Database / Runtime Files

- By default the app stores history in `backend/data/analyses.db`. This path is ignored by `.gitignore` to keep repository history clean. You can override it with the `ANALYSES_DB` environment variable.
- Generated reports and runtime logs are ignored (`*.pdf`, `*.log`).

## Usage

1. Go to the home page and paste or select a sample job description (or use the `Samples` page).
2. Upload a candidate resume (`.pdf` or `.docx`).
3. Click `Analyze Resume` — results are shown immediately with a match score and breakdown.
4. Download the PDF report if needed and inspect the `History` for prior analyses.

## Development & Contribution

- Run tests (if present) and linters before opening a PR.
- Keep commits small and documented. Example commit message:

```
feat: add insights chart to dashboard
```

- If the virtual environment was accidentally committed, remove it and add it to `.gitignore`:

```bash
git rm -r --cached .venv
git commit -m "chore: stop tracking virtual environment"
```

## Preparing for GitHub

- Pin dependencies before publishing:

```bash
pip freeze > requirements.txt
```

- Ensure the following are ignored in `.gitignore`: `.venv/`, `backend/data/`, `*.pdf`, `*.log`, `.env`.

## Contact
Author: TechCoder-Abhi — https://github.com/TechCoder-Abhi
