import os
from collections import Counter
from flask import Blueprint, render_template, request, send_file, redirect, url_for, current_app
from .controllers import analyze
from . import db as _db

bp = Blueprint('main', __name__)

@bp.route('/download')
def download():
    try:
        return send_file(os.path.abspath('resume_report.pdf'), as_attachment=True)
    except FileNotFoundError:
        return "Report not found. Please analyze a resume first.", 404

@bp.route('/history')
def history():
    analyses = _db.get_all_analyses()
    return render_template('history.html', analyses=analyses)


@bp.route('/samples')
def samples():
    samples = [
        {
            'title': 'Backend Engineer',
            'summary': 'Python, Flask, SQL, Docker, AWS',
            'text': 'We are looking for a backend engineer with strong Python and Flask skills, plus SQL, Docker, and AWS experience.'
        },
        {
            'title': 'Frontend Engineer',
            'summary': 'React, JavaScript, HTML, CSS',
            'text': 'We need a frontend engineer with React, JavaScript, HTML, CSS, and accessibility experience.'
        },
        {
            'title': 'ML / Data Role',
            'summary': 'Python, pandas, numpy, machine learning',
            'text': 'We are hiring a data scientist with Python, pandas, numpy, machine learning, and scikit-learn experience.'
        },
    ]
    return render_template('samples.html', samples=samples)


@bp.route('/insights')
def insights():
    analyses = _db.get_all_analyses()
    scores = [a['match'] for a in analyses]
    total = len(analyses)
    avg = round(sum(scores) / total, 2) if total else 0
    best = max(scores) if scores else 0
    latest = analyses[0] if analyses else None

    skill_counter = Counter()
    for analysis in analyses:
        skill_counter.update(analysis.get('matched', []))

    top_skills = skill_counter.most_common(8)
    recent_labels = [a['timestamp'][:16].replace('T', ' ') for a in analyses[:8]][::-1]
    recent_scores = [a['match'] for a in analyses[:8]][::-1]

    return render_template(
        'insights.html',
        total=total,
        avg=avg,
        best=best,
        latest=latest,
        top_skills=top_skills,
        recent_labels=recent_labels,
        recent_scores=recent_scores,
    )

@bp.route('/clear_history')
def clear_history():
    _db.clear_history()
    return redirect(url_for('main.history'))


@bp.route('/delete/<int:analysis_id>', methods=['POST'])
def delete_analysis(analysis_id):
    _db.delete_analysis(analysis_id)
    return redirect(url_for('main.history'))


@bp.route('/dashboard')
def dashboard():
    analyses = _db.get_all_analyses()
    # Simple summary stats
    total = len(analyses)
    avg = round(sum(a['match'] for a in analyses) / total, 2) if total > 0 else 0
    return render_template('dashboard.html', total=total, avg=avg)


@bp.route('/', methods=['GET', 'POST'])
def index():
    result = None
    job_desc = request.args.get('sample', '').strip()
    error = None

    if request.method == 'POST':
        resume = request.files.get('resume')
        job_desc = request.form.get('job', '').strip()

        if not resume or resume.filename == '':
            error = 'Please upload a resume PDF or DOCX.'
        elif not job_desc:
            error = 'Please enter a job description.'
        else:
            try:
                resume_text = analyze.extract_text_from_file(resume, resume.filename)
                job_text = job_desc.lower()
                result = analyze.compute_match_and_result(resume_text, job_text)
                analyze.generate_pdf(result)
                _db.save_analysis(result['match'], result['matched'], result['missing'])
            except Exception as e:
                # Log full exception with stacktrace to backend log
                current_app.logger.exception('Error processing resume')
                # Show generic message to user
                error = 'An internal error occurred while processing the resume. Please try a different file or contact support.'

    return render_template('index.html', result=result, job_desc=job_desc, error=error)
