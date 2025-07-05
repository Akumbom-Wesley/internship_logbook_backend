from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from apps.logbooks.models import Logbook
from datetime import datetime

def generate_logbook_pdf(logbook: Logbook):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    elements = []
    styles = getSampleStyleSheet()

    # Custom style for wrapping text in table cells
    cell_style = ParagraphStyle(
        name='CellStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        wordWrap='CJK',  # Enables text wrapping
        leading=10,
    )

    internship = logbook.internship
    student = internship.student
    user = student.user
    company = internship.company
    supervisor = internship.supervisor

    # ----------- HEADER SECTION -----------
    elements.append(Paragraph("STUDENT INTERNSHIP LOG BOOK", styles['Heading1']))
    elements.append(Spacer(1, 12))

    header_data = [
        ["NAME:", user.full_name],
        ["REGISTRATION NUMBER:", student.matricule_num],
        ["DEPARTMENT:", student.department.name],
        ["ATTACHMENT PERIOD:", f"{internship.start_date.strftime('%d %B, %Y')} to {internship.end_date.strftime('%d %B, %Y')}"],
        ["COMPANY'S NAME:", company.name],
        ["ADDRESS:", company.address],
        ["PHONE NUMBER:", company.contact],
        ["DEPARTMENT/DIVISION:", company.division],
    ]
    header_table = Table(header_data, colWidths=[150, 350])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # ----------- DAILY ATTACHMENT RECORDS SECTION -----------
    elements.append(Paragraph("DAILY ATTACHMENT RECORDS", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # ----------- WEEKLY LOGS SECTION -----------
    for week in logbook.weekly_logs.all().order_by('week_no'):
        week_title = Paragraph(f"Week {week.week_no}", styles['Heading3'])
        elements.append(week_title)
        elements.append(Spacer(1, 8))

        # Table headers for the week
        week_table_data = [["Day", "Activity Description"]]

        # Initialize dictionary for weekday ordering
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        week_log_dict = {day: "No activity recorded" for day in weekdays}

        # Populate dictionary with entries
        for entry in week.logbook_entries.all():
            day_name = entry.created_at.strftime("%A")
            if day_name in week_log_dict:
                week_log_dict[day_name] = entry.description

        # Create table rows with wrapped text
        for day in weekdays:
            description = Paragraph(week_log_dict[day], cell_style)
            week_table_data.append([day, description])

        week_table = Table(week_table_data, colWidths=[100, 400])
        week_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(week_table)
        elements.append(Spacer(1, 20))

    # ----------- SIGNATURE SECTION -----------
    signature_text = f"""
    Intern's Signature: ____________________________<br/><br/>
    Field Supervisor's Signature: ____________________________<br/><br/>
    Name: {supervisor.user.full_name}<br/>
    Company's Stamp: ____________________________<br/><br/>
    Date: {datetime.today().strftime('%d %B, %Y')}
    """
    elements.append(Paragraph(signature_text, styles['Normal']))
    elements.append(Spacer(1, 20))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer