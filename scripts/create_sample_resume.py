from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Sample Resume - John Doe', ln=True)
pdf.ln(5)
pdf.set_font('Arial', size=12)
pdf.multi_cell(0, 8, 'Experienced Python developer with skills in Python, Flask, SQL, Docker, AWS, and Machine Learning.')
pdf.output('sample_resume.pdf')
print('Created sample_resume.pdf')
