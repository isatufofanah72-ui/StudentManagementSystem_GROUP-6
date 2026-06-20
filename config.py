"""
Config Module
Centralizes system branding layout metrics and foundational criteria rules configurations.
"""
SYSTEM_NAME = "Sierra Leone Student Performance Dashboard (SDG 4)"
FONT_FAMILY = "Tahoma"

# Dynamic Grading Architecture matrix mapping rules array
GRADE_SCALE = [
    {"min": 90, "grade": "A+", "gpa": 4.0, "status": "Excellent"},
    {"min": 84, "grade": "A",  "gpa": 4.0, "status": "Excellent"},
    {"min": 80, "grade": "A-", "gpa": 3.7, "status": "Very Good"}, 
    {"min": 74, "grade": "B+", "gpa": 3.3, "status": "Very Good"},
    {"min": 70, "grade": "B",  "gpa": 3.0, "status": "Good"},
    {"min": 64, "grade": "B-", "gpa": 2.7, "status": "Good"},
    {"min": 60, "grade": "C+", "gpa": 2.3, "status": "Satisfactory"},
    {"min": 54, "grade": "C",  "gpa": 2.0, "status": "Pass"},
    {"min": 50, "grade": "C-", "gpa": 1.7, "status": "Pass"},
    {"min": 0,  "grade": "F",  "gpa": 0.0, "status": "Fail"}
]