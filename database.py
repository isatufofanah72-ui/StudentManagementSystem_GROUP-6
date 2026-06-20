"""
Database Management Module (PostgreSQL Edition)
Establishes relational data processing pipelines with pgAdmin/PostgreSQL.
Seeds 20 structured records to fulfill the evaluation brief.
"""
import psycopg2
from datetime import datetime

# Adjust these credentials to match your local pgAdmin settings
DB_SETTINGS = {
    "dbname": "academic_records",
    "user": "postgres",
    "password": "ronaldo",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    """Returns an active connection instance to the local PostgreSQL database server."""
    return psycopg2.connect(**DB_SETTINGS)

def initialize_database():
    """Initializes standard PostgreSQL tables and structures tracking records."""
    # Connect to default postgres database first to ensure academic_records exists
    temp_conn = psycopg2.connect(
        dbname="postgres",
        user=DB_SETTINGS["user"],
        password=DB_SETTINGS["password"],
        host=DB_SETTINGS["host"],
        port=DB_SETTINGS["port"]
    )
    temp_conn.autocommit = True
    temp_cursor = temp_conn.cursor()
    
    # Create database if it doesn't exist
    temp_cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'academic_records'")
    if not temp_cursor.fetchone():
        temp_cursor.execute("CREATE DATABASE academic_records")
        
    temp_cursor.close()
    temp_conn.close()

    # Now connect to the academic_records database to create tables
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. User Authentication Matrix Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL
    )
    """)
    
    # 2. Main Student Performance Records Master Data Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id VARCHAR(30) PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        gender VARCHAR(15) NOT NULL,
        assignment NUMERIC(5,2) NOT NULL,
        exam NUMERIC(5,2) NOT NULL,
        total NUMERIC(5,2) NOT NULL,
        grade VARCHAR(5) NOT NULL,
        gpa NUMERIC(3,2) NOT NULL,
        status VARCHAR(20) NOT NULL,
        contact VARCHAR(100) NOT NULL,
        created_date DATE NOT NULL
    )
    """)
    
    # Populate Default Administrative User
    cursor.execute("INSERT INTO users VALUES ('admin', 'admin123') ON CONFLICT (username) DO NOTHING")
    
    # Check row count and seed minimum 20 records
    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        sample_students = [
            ("LU-001", "Amadu Kamara", "Male", 34.0, 52.0, "Active", "amadu@example.com", "2026-02-10"),
            ("LU-002", "Fatmata Bangura", "Female", 38.0, 56.0, "Active", "fatmata@example.com", "2026-02-15"),
            ("LU-003", "Sahr Jiah", "Male", 22.0, 41.0, "Active", "sahr@example.com", "2026-03-01"),
            ("LU-004", "Isatu Conteh", "Female", 15.0, 32.0, "Pending", "isatu@example.com", "2026-03-05"),
            ("LU-005", "John Sesay", "Male", 31.0, 48.0, "Active", "john@example.com", "2026-03-12"),
            ("LU-006", "Zainab Turay", "Female", 29.0, 45.0, "Inactive", "zainab@example.com", "2026-04-02"),
            ("LU-007", "Emmanuel Cole", "Male", 12.0, 25.0, "Active", "emmanuel@example.com", "2026-04-10"),
            ("LU-008", "Mariama Barrie", "Female", 35.0, 58.0, "Active", "mariama@example.com", "2026-04-18"),
            ("LU-009", "Mohamed Kallon", "Male", 26.0, 38.0, "Pending", "mohamed@example.com", "2026-05-01"),
            ("LU-010", "Alie Mansaray", "Male", 33.0, 51.0, "Active", "alie@example.com", "2026-05-06"),
            ("LU-011", "Kadiatu Koroma", "Female", 20.0, 31.0, "Inactive", "kadiatu@example.com", "2026-05-15"),
            ("LU-012", "Samuel Kargbo", "Male", 37.0, 53.0, "Active", "samuel@example.com", "2026-05-22"),
            ("LU-013", "Grace Williams", "Female", 39.0, 57.0, "Active", "grace@example.com", "2026-05-29"),
            ("LU-014", "Hassan Dumbuya", "Male", 18.0, 28.0, "Pending", "hassan@example.com", "2026-06-01"),
            ("LU-015", "Miatta Fofanah", "Female", 28.0, 42.0, "Active", "miatta@example.com", "2026-06-03"),
            ("LU-016", "Mustapha Kanu", "Male", 32.0, 49.0, "Active", "mustapha@example.com", "2026-06-05"),
            ("LU-017", "Rebecca Taylor", "Female", 24.0, 36.0, "Active", "rebecca@example.com", "2026-06-08"),
            ("LU-018", "Abdulai Sow", "Male", 14.0, 22.0, "Inactive", "abdulai@example.com", "2026-06-10"),
            ("LU-019", "Patricia Thomas", "Female", 36.0, 50.0, "Active", "patricia@example.com", "2026-06-12"),
            ("LU-020", "Festus Rogers", "Male", 30.0, 44.0, "Active", "festus@example.com", "2026-06-14")
        ]
        
        for item in sample_students:
            tot = item[3] + item[4]
            # Map your requested grade boundaries
            if tot >= 90: gd, gp = "A+", 4.0
            elif tot >= 84: gd, gp = "A", 4.0
            elif tot >= 80: gd, gp = "A-", 3.7
            elif tot >= 74: gd, gp = "B+", 3.3
            elif tot >= 70: gd, gp = "B", 3.0
            elif tot >= 64: gd, gp = "B-", 2.7
            elif tot >= 60: gd, gp = "C+", 2.3
            elif tot >= 54: gd, gp = "C", 2.0
            elif tot >= 50: gd, gp = "C-", 1.7
            else: gd, gp = "F", 0.0
            
            cursor.execute(
                "INSERT INTO records VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                (item[0], item[1], item[2], item[3], item[4], tot, gd, gp, item[5], item[6], item[7])
            )
            
    conn.commit()
    cursor.close()
    conn.close()