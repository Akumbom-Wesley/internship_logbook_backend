from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from apps.evaluations.models import Evaluation


def generate_evaluation_pdf(evaluation: Evaluation):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header with official information
    def draw_header():
        y = height - 30

        # Republic info
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "REPUBLIC OF CAMEROON")
        c.drawString(400, y, "REPUBLIQUE DU CAMEROUN")
        y -= 15
        c.setFont("Helvetica", 9)
        c.drawString(50, y, "Peace – Work – Fatherland")
        c.drawString(400, y, "Paix – Travail - Patrie")
        y -= 30

        # Ministry info
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "MINISTRY OF HIGHER EDUCATION")
        c.drawString(350, y, "MINISTERE DE L'ENSEIGNEMENT SUPERIEUR")
        y -= 30

        # University info
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, y, "THE UNIVERSITY OF BAMENDA")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, y, "P.O. Box 39, Bambili")
        y -= 12
        c.drawCentredString(width / 2, y, "Fax (237) 233 366 030 - Website: www.uniba.cm")
        y -= 15
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, y, "L'UNIVERSITE DE BAMENDA")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, y, "B.P. 39, Bambili")
        y -= 12
        c.drawCentredString(width / 2, y, "Fax (237) 233 366 030 - Website: www.uniba.cm")
        y -= 30

        # Institute info
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "National Higher Polytechnic Institute (NAHPI)")
        c.drawString(350, y, "Ecole Nationale Supérieure Polytechnique (ENSPB)")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "(School of Engineering)")
        c.drawString(350, y, "(Ecole d'Ingénieurs)")
        y -= 25

        # Staff info
        c.setFont("Helvetica", 8)
        staff_info = [
            "Director : Fidelis Cho-Ngwa, Professor",
            "Deputy Director : Nfah Mbaka Eustace, Assoc. Professor",
            "HD/ Academic Affairs, Research and Cooperation: Fozao Kennedy Folepai, Assoc. Professor",
            "HD/ Student Records, Studies and Internship : Fautso Kuiate Gaetan, Assoc. Professor",
            "HD/ Continuous and Distant Training : Dr. Mih Thomas Attia",
            "HD/ Administrative and Financial Affairs : Mrs. Bin Marcella Njang"
        ]

        for info in staff_info:
            c.drawString(50, y, info)
            y -= 12

        return y - 30

    y = draw_header()

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, "INTERNSHIP EVALUATION FORM")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y,
                        "This evaluation form is to be filled by the field supervisor, stamped with the official seal and returned to the institute")
    y -= 10
    c.drawCentredString(width / 2, y, "in a sealed envelop.")
    y -= 30

    # Section A: INTERN DETAILS
    internship = evaluation.internship
    student = internship.student.user

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "A. INTERN DETAILS")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Name: {getattr(student, 'full_name', 'N/A')}")
    y -= 15
    c.drawString(50, y, f"Intern ID: {internship.student.matricule_num}")
    y -= 15
    c.drawString(50, y, f"Programme: {getattr(internship.student, 'programme', 'N/A')}")
    y -= 15
    c.drawString(50, y, f"Internship Duration From: {internship.start_date} To: {internship.end_date}")
    y -= 25

    # Section B: COMPANY DETAILS
    company = internship.company
    supervisor = internship.supervisor

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "B. COMPANY DETAILS")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Company's Name: {company.name}")
    y -= 15
    c.drawString(50, y, f"Department/Division: {getattr(company, 'department', 'N/A')}")
    y -= 15
    c.drawString(50, y, f"Field Supervisor Name: {getattr(supervisor.user, 'full_name', 'N/A')}")
    y -= 15
    c.drawString(50, y, f"Contact Number: {getattr(supervisor.user, 'phone', 'N/A')}")
    y -= 15
    c.drawString(50, y, f"Designation: {getattr(supervisor, 'designation', 'N/A')}")
    c.drawString(350, y, f"Email Address: {supervisor.user.email}")
    y -= 25

    # Section C: JOB DESCRIPTION
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "C. JOB DESCRIPTION")
    y -= 20

    c.setFont("Helvetica", 11)
    job_description = getattr(internship, 'job_description', 'No job description provided.')
    job_desc_lines = job_description.split('\n')[:4]  # Take first 4 lines
    for i, line in enumerate(job_desc_lines, 1):
        c.drawString(50, y, f"{i}. {line}")
        y -= 15

    # Fill remaining lines if less than 4
    for i in range(len(job_desc_lines) + 1, 5):
        c.drawString(50, y, f"{i}.")
        y -= 15

    y -= 10

    # Section D: EVALUATION
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "D. EVALUATION")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y,
                 "Evaluation of student's qualities during his/her internship according to the point breakdown below. Select one evaluation")
    y -= 12
    c.drawString(50, y, "level for each area and assign a score against each item listed.")
    y -= 20

    # Point Breakdown
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Point Breakdown")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Poor : 1 pt    Underdevelop : 2 pts    Average : 3 pts    Good : 4 pts    Outstanding : 5 pts")
    y -= 25

    # Evaluation Categories - Display all categories with proper formatting
    categories = evaluation.categories.all().order_by('template__order')

    if not categories.exists():
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "No evaluation categories found.")
        y -= 20
    else:
        for category in categories:
            # Check if we need a new page
            if y < 200:  # Leave space for category content
                c.showPage()
                y = height - 50

            # Category header
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, f"{category.name.upper()}")
            c.drawString(450, y, "POINTS")
            y -= 15

            # Category subfields
            subfields = category.subfields.all().order_by('template__order')

            for subfield in subfields:
                c.setFont("Helvetica", 10)
                c.drawString(50, y, subfield.name)
                c.drawString(470, y, str(subfield.score))
                y -= 12

            # Category total using the calculated subfields_total from the model
            y -= 5
            c.setFont("Helvetica-Bold", 10)
            c.drawString(400, y, f"Total {category.subfields_total}/20")
            y -= 20

        # Overall Total Score using the calculated total_score from the model
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, f"TOTAL {evaluation.total_score}/100")
    y -= 30

    # Additional Comments
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "ADDITIONAL COMMENTS/AREAS OF DEVELOPMENT")
    y -= 20

    c.setFont("Helvetica", 10)
    if evaluation.comments:
        lines = evaluation.comments.split('\n')
        for line in lines:
            if y < 100:  # Start new page if needed
                c.showPage()
                y = height - 50
            c.drawString(50, y, line)
            y -= 15

    y -= 30

    # Signature section
    if y < 100:
        c.showPage()
        y = height - 50

    c.setFont("Helvetica", 11)
    supervisor_name = getattr(supervisor.user, 'full_name', 'N/A')
    c.drawString(50, y, f"Name: {supervisor_name}")
    y -= 30

    # Handle signature date - might not exist yet
    signature_date = getattr(evaluation, 'supervisor_signature_date', 'Not signed')
    c.drawString(50, y, f"Field Supervisor's Signature: _________________________ Date: {signature_date}")
    y -= 30
    c.drawString(50, y, "Company's Stamp: _________________________________________________________________")

    c.showPage()
    c.save()
    buffer.seek(0)  # Reset buffer position
    return buffer