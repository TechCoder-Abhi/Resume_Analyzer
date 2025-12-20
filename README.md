# Resume Analyzer

A professional Flask-based web application that analyzes resumes against job descriptions to identify **matched skills, missing skills, and show overall compatibility score.**

## Features

- **📄 Multi-Format Resume Support**: Upload resumes in PDF or DOCX formats
- **🎯 Intelligent Skill Matching**: Advanced keyword extraction and weighted scoring algorithm
- **📊 Comprehensive Analysis Reports**: Detailed match percentages with matched/missing skills breakdown
- **📥 PDF Report Generation**: Downloadable professional analysis reports using FPDF
- **📚 Analysis History**: persevering of all analyses with SQLite database
- **🗑️ History Management**: Clear history functionality with confirmation dialogs

## 🛠️ Technologies Used

### Backend
- **Flask 3.1+**: Lightweight WSGI web application framework
- **Python 3.8+**: Core programming language
- **SQLite 3**: Embedded database for data persevering
- **PyPDF2**: PDF text extraction library
- **python-docx**: Microsoft Word document processing
- **spaCy**: Industrial-strength NLP library (for future enhancements)
- **FPDF**: PDF generation library

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Interactive user interface enhancements

### Development Tools
- **Git**: Version control system
- **pip**: Python package manager
- **Virtual Environment**: Isolated Python environment

## Installation

1. Clone the repository

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open http://localhost:5000 in your browser

## Usage

1. Upload a PDF or DOCX resume
2. Paste the job description
3. Click "Analyze Resume"
4. View the match percentage and skill breakdown
5. Download the PDF report
6. Use "New Role" to clear the job description for a new analysis
7. Click "View History" to see past analyses
8. Use the "Clear History" button to remove all stored analyses

## 👤 Author

**TechCoder-Abhi**
- GitHub: [@TechCoder-Abhi](https://github.com/TechCoder-Abhi)
- Project: [Resume Analyzer](https://github.com/TechCoder-Abhi/Resume_Analyzer)

---

⭐ **Star this repository** if you found it helpful!

📧 **Feedback**: Open an issue for bugs or feature requests