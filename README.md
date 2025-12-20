# AI Resume Analyzer

A professional Flask-based web application that analyzes resumes against job descriptions using AI-powered skill matching.

## Features

- Upload PDF or DOCX resumes for analysis
- Compare against job descriptions
- Weighted skill matching with importance scores
- Generate downloadable PDF reports
- Clean, responsive web interface
- Error handling for invalid inputs

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open http://localhost:5000 in your browser

## Usage

1. Upload a PDF or DOCX resume
2. Paste the job description
3. Click "Analyze Resume"
4. View the match percentage and skill breakdown
5. Download the PDF report
6. Use "New Role" to clear the job description for a new analysis

## Technologies

- Flask
- PyPDF2
- python-docx
- spaCy
- FPDF
- HTML/CSS/JavaScript

## License

MIT License