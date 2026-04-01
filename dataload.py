import oracledb
import csv
import os

# --- SETUP ---
LIB_DIR = r"C:\oracle\instantclient_23_0"  
DB_USER = "system" 
DB_PASS = "21466K" 
DB_DSN  = "localhost:1521/XE"

# Initialize Thick Mode (Required for FreeSQL/Cloud)
oracledb.init_oracle_client(lib_dir=LIB_DIR)

def bulk_load_student(file_path):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        sql = "INSERT INTO Student (StudentID, Fname, Lname, DOB, Email, Phone, AdmissionDate) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, TO_DATE(:7, 'YYYY-MM-DD'))"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


def bulk_load_course(file_path):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        sql = "INSERT INTO Course (CourseID, CourseName, Credits, Description) VALUES (:1, :2, :3, :4)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def bulk_load_enrollment(file_path):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        sql = "INSERT INTO Enrollment (EnrollmentID, StudentID, CourseID, Status) VALUES (:1, :2, :3, :4)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def bulk_load_grade(file_path):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        sql = "INSERT INTO Grade (EnrollmentID, Grade, LetterGrade) VALUES (:1, :2, :3)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()        

def bulk_load_attendance(file_path):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        sql = "INSERT INTO Attendance (EnrollmentID, AttendanceRate) VALUES (:1, :2)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()   


# Run the function
dir = os.getcwd()

file_path = os.path.join(dir, "data", "student_information.csv")
bulk_load_student(file_path)

file_path = os.path.join(dir, "data", "course_information.csv")
bulk_load_course(file_path)

file_path = os.path.join(dir, "data", "enrollment_information.csv")
bulk_load_enrollment(file_path)

file_path = os.path.join(dir, "data", "grade_information.csv")
bulk_load_grade(file_path)

file_path = os.path.join(dir, "data", "attendance_information.csv")
bulk_load_attendance(file_path)