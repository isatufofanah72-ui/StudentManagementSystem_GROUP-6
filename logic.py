"""
Logic Module - Processing and Output Generation Module
Calculates metrics, manages input data insertions, and handles advanced PostgreSQL dynamic reporting.
"""
from datetime import datetime, timedelta
import database
import config
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def validate_scores(assignment, exam):
    """Checks continuous assessment constraints boundaries[cite: 149]."""
    try:
        a = float(assignment)
        e = float(exam)
    except ValueError:
        return False, "Scores input entries must contain valid numerical structures."
    if not (0 <= a <= 40) or not (0 <= e <= 60):
        return False, "Boundaries Error: Assignment [0-40], Exam [0-60]."
    return True, "Valid"

def calculate_metrics(assignment, exam):
    """Calculates final grade boundaries and GPA standings from config arrays."""
    total = float(assignment) + float(exam)
    for tier in config.GRADE_SCALE:
        if total >= tier["min"]:
            return {"total": total, "grade": tier["grade"], "gpa": tier["gpa"]}
    return {"total": total, "grade": "F", "gpa": 0.0}

def insert_student_record(sid, name, gender, assignment, exam, status, contact):
    """Backend insertion handler to validate and commit a new entry row into PostgreSQL."""
    # 1. Run structural input score data validations
    is_valid, msg = validate_scores(assignment, exam)
    if not is_valid:
        return False, msg
        
    if not sid.strip() or not name.strip() or not contact.strip():
        return False, "All text entry input fields must be filled out completely."
        
    # 2. Compute variables dynamically
    metrics = calculate_metrics(assignment, exam)
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 3. Connect and execute insert query statement securely
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO records (id, full_name, gender, assignment, exam, total, grade, gpa, status, contact, created_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (sid.strip(), name.strip(), gender, float(assignment), float(exam), 
             metrics["total"], metrics["grade"], metrics["gpa"], status, contact.strip(), today_str)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Student record successfully added to PostgreSQL server!"
    except Exception as e:
        return False, f"Database Integrity Error (Check if ID already exists):\n{e}"

def fetch_filtered_records(search_term="", gender="All", status="All", date_range="All"):
    """Builds PostgreSQL relational data queries using proper tokenization styles."""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM records WHERE (id ILIKE %s OR full_name ILIKE %s)"
    params = [f"%{search_term}%", f"%{search_term}%"]
    
    if gender != "All":
        query += " AND gender = %s"
        params.append(gender)
    if status != "All":
        query += " AND status = %s"
        params.append(status)
        
    if date_range != "All":
        today = datetime.now()
        if date_range == "Daily":
            start_date = today.strftime('%Y-%m-%d')
        elif date_range == "Weekly":
            start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        elif date_range == "Monthly":
            start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        elif date_range == "Yearly":
            start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        query += " AND created_date >= %s"
        params.append(start_date)
        
    query += " ORDER BY id ASC"
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def generate_pdf_report(scope_type):
    """Compiles multi-field academic summary ledgers into hardcopy PDF sheets."""
    data = fetch_filtered_records(date_range=scope_type)
    filename = f"Academic_Report_{scope_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph(f"<b>LIMKOKWING UNIVERSITY PORTAL REPORT - {scope_type.upper()}</b>", styles['Title']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Region: Sierra Leone (SDG 4)", styles['Normal']))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(f"<b>Total Evaluated Student Matrices:</b> {len(data)} records", styles['Heading3']))
    story.append(Spacer(1, 10))
    
    table_content = [["ID", "Name", "Gender", "Total", "Grade", "Status", "Created"]]
    for row in data:
        table_content.append([row[0], row[1], row[2], str(row[5]), row[6], row[8], str(row[10])])
        
    report_table = Table(table_content, colWidths=[55, 120, 60, 45, 45, 60, 80])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    
    story.append(report_table)
    doc.build(story)
    return filename