-- ============================================================================
-- LIMKOKWING UNIVERSITY OF CREATIVE TECHNOLOGY - SIERRA LEONE [cite: 1, 2]
-- FACULTY OF INFORMATION & COMMUNICATIONS TECHNOLOGY [cite: 4, 5]
-- MODULE: PROG103 - PRINCIPLE OF STRUCTURED PROGRAMMING [cite: 7, 8]
-- PROJECT: STRUCTURED DIGITAL SOLUTION FOR PUBLIC SERVICE (SDG 4) [cite: 13, 42]
-- DATABASE SPECIFICATION MANAGEMENT SCRIPT (POSTGRESQL DIALECT)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CLEANUP & ISOLATION DROP OPERATIONS
-- Removes preexisting tables to ensure clean, idempotent structural schema builds.
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS records CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ----------------------------------------------------------------------------
-- 2. TABLE CONFIGURATION STRUCTURES
-- ----------------------------------------------------------------------------

-- A. Administrative Authentication Portals Storage Matrix Table
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);

-- B. Main Student Performance Records Master Data Table [cite: 76]
CREATE TABLE records (
    id VARCHAR(30) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender VARCHAR(15) NOT NULL,
    assignment NUMERIC(5,2) NOT NULL CHECK (assignment BETWEEN 0.0 AND 40.0), -- Continuous Assessment Cap
    exam NUMERIC(5,2) NOT NULL CHECK (exam BETWEEN 0.0 AND 60.0),             -- Final Exam Cap
    total NUMERIC(5,2) NOT NULL,                                              -- Derived Assignment + Exam
    grade VARCHAR(5) NOT NULL,                                                -- Config.py Matrix String Lookups
    gpa NUMERIC(3,2) NOT NULL,                                                -- Grade Point Average Weight
    status VARCHAR(20) NOT NULL,                                              -- System Status: Active, Inactive, Pending
    contact VARCHAR(100) NOT NULL,                                            -- Contact Information (Email/Phone)
    created_date DATE NOT NULL DEFAULT CURRENT_DATE                           -- Audit Timeline Fields Tracking
);

-- ----------------------------------------------------------------------------
-- 3. ADMINISTRATIVE MASTER IDENTITIES SEEDING
-- ----------------------------------------------------------------------------
INSERT INTO users (username, password) 
VALUES ('admin', 'admin123')
ON CONFLICT (username) DO NOTHING;

-- ----------------------------------------------------------------------------
-- 4. EVALUATION DATA COMPLIANCE SEEDING (MINIMUM 20 STRUCTURAL DATA RECORDS) [cite: 86]
-- Maps precise total score evaluation tiers directly to your grade boundaries:
-- >=90:A+, >=84:A, >=80:A-, >=74:B+, >=70:B, >=64:B-, >=60:C+, >=54:C, >=50:C-, <50:F
-- ----------------------------------------------------------------------------
INSERT INTO records (id, full_name, gender, assignment, exam, total, grade, gpa, status, contact, created_date)
VALUES 
    ('LU-001', 'Amadu Kamara', 'Male', 34.0, 52.0, 86.0, 'A', 4.0, 'Active', 'amadu@example.com', '2026-02-10'),
    ('LU-002', 'Fatmata Bangura', 'Female', 38.0, 56.0, 94.0, 'A+', 4.0, 'Active', 'fatmata@example.com', '2026-02-15'),
    ('LU-003', 'Sahr Jiah', 'Male', 22.0, 41.0, 63.0, 'C+', 2.3, 'Active', 'sahr@example.com', '2026-03-01'),
    ('LU-004', 'Isatu Conteh', 'Female', 15.0, 32.0, 47.0, 'F', 0.0, 'Pending', 'isatu@example.com', '2026-03-05'),
    ('LU-005', 'John Sesay', 'Male', 31.0, 48.0, 79.0, 'B+', 3.3, 'Active', 'john@example.com', '2026-03-12'),
    ('LU-006', 'Zainab Turay', 'Female', 29.0, 45.0, 74.0, 'B+', 3.3, 'Inactive', 'zainab@example.com', '2026-04-02'),
    ('LU-007', 'Emmanuel Cole', 'Male', 12.0, 25.0, 37.0, 'F', 0.0, 'Active', 'emmanuel@example.com', '2026-04-10'),
    ('LU-008', 'Mariama Barrie', 'Female', 35.0, 58.0, 93.0, 'A+', 4.0, 'Active', 'mariama@example.com', '2026-04-18'),
    ('LU-009', 'Mohamed Kallon', 'Male', 26.0, 38.0, 64.0, 'B-', 2.7, 'Pending', 'mohamed@example.com', '2026-05-01'),
    ('LU-010', 'Alie Mansaray', 'Male', 33.0, 51.0, 84.0, 'A', 4.0, 'Active', 'alie@example.com', '2026-05-06'),
    ('LU-011', 'Kadiatu Koroma', 'Female', 20.0, 31.0, 51.0, 'C-', 1.7, 'Inactive', 'kadiatu@example.com', '2026-05-15'),
    ('LU-012', 'Samuel Kargbo', 'Male', 37.0, 53.0, 90.0, 'A+', 4.0, 'Active', 'samuel@example.com', '2026-05-22'),
    ('LU-013', 'Grace Williams', 'Female', 39.0, 57.0, 96.0, 'A+', 4.0, 'Active', 'grace@example.com', '2026-05-29'),
    ('LU-014', 'Hassan Dumbuya', 'Male', 18.0, 28.0, 46.0, 'F', 0.0, 'Pending', 'hassan@example.com', '2026-06-01'),
    ('LU-015', 'Miatta Fofanah', 'Female', 28.0, 42.0, 70.0, 'B', 3.0, 'Active', 'miatta@example.com', '2026-06-03'),
    ('LU-016', 'Mustapha Kanu', 'Male', 32.0, 49.0, 81.0, 'A-', 3.7, 'Active', 'mustapha@example.com', '2026-06-05'),
    ('LU-017', 'Rebecca Taylor', 'Female', 24.0, 36.0, 60.0, 'C+', 2.3, 'Active', 'rebecca@example.com', '2026-06-08'),
    ('LU-018', 'Abdulai Sow', 'Male', 14.0, 22.0, 36.0, 'F', 0.0, 'Inactive', 'abdulai@example.com', '2026-06-10'),
    ('LU-019', 'Patricia Thomas', 'Female', 36.0, 50.0, 86.0, 'A', 4.0, 'Active', 'patricia@example.com', '2026-06-12'),
    ('LU-020', 'Festus Rogers', 'Male', 30.0, 44.0, 74.0, 'B+', 3.3, 'Active', 'festus@example.com', '2026-06-14')
ON CONFLICT (id) DO NOTHING;

-- ----------------------------------------------------------------------------
-- 5. VERIFICATION VALIDATION QUERIES
-- Runs system verification checks on the preloaded data to confirm correct setup.
-- ----------------------------------------------------------------------------

-- Check A: Verify User Credential Initialization Matrix Status
SELECT username, '••••••••' AS hidden_password_hash FROM users;

-- Check B: Sample Multi-parameter Filtering Engine Simulation (Lecturer Condition Test Example)
SELECT id, full_name, gender, total, grade, status, created_date 
FROM records 
WHERE gender = 'Female' 
  AND status = 'Active'
ORDER BY total DESC;

-- Check C: Verify Grade Category Distributions
SELECT grade, COUNT(*) as student_count, ROUND(AVG(total), 2) as average_score
FROM records
GROUP BY grade
ORDER BY average_score DESC;