'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

import streamlit as st
import oracledb
import pandas as pd

# --- DATABASE SETUP ---
# Update this path to your local Instant Client folder
LIB_DIR = "" # Your Instant Client Path
DB_USER = "" # DB Username
DB_PASS = "" # DB Password
DB_DSN  = "" # DSN Here


# Initialize Oracle Client for Thick Mode
@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")


init_db()


def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)


# --- STREAMLIT UI ---
st.title("University Student Performance Enrollment Database")
st.subheader("Get Student and Course Information Here")

# --- MAIN INPUT MENUS ---

student_menu = ["Student General Info", "Student Courses", "Student GPA", "Student Attendance Rate"]
course_menu = ["Find Course", "Course Enrollment Info"]
student_choice = st.sidebar.selectbox("Student Info", student_menu)
course_choice = st.sidebar.selectbox("Course Info", course_menu)

select = ["Student Information", "Course Information"]
bubble = st.pills("Data Options", select)

# --- ALL OF THE STUDENT RELATED QUERIES ---
if bubble == "Student Information":
    
    # --- FIND STUDENT INFO ---
    if student_choice == "Student General Info":
        st.write("### Find Student's Information")
        input_option = st.pills("Input Option", ["ID", "Name"]) # allows user to input either ID or Name depending on what they have
        
        if input_option == "ID": 
            studID = st.text_input("Enter Student's ID")
            if st.button("Find Student"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT * from STUDENT WHERE StudentID = :1", [studID])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "DOB", "Email", "Phone", "Admission_Date"])
                    conn.commit()
                    cur.close()
                    conn.close()
                    if data:
                        st.table(df, hide_header= False)
                        st.success(f"Successfully found Student with the ID {studID}!!")
                    else:
                        st.info("No records found.")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        elif input_option == "Name":
            fname = st.text_input("Enter Student's First Name")
            lname = st.text_input("Enter Student's Last Name")

            if st.button("Find Student"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT * from STUDENT WHERE Fname = :1 AND Lname = :2", [fname, lname])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "DOB", "Email", "Phone", "Admission_Date"])
                    conn.commit()
                    cur.close()
                    conn.close()
                    if data:
                        st.table(df, hide_header= False)
                    else:
                        st.info("No records found.")
                        st.success(f"Successfully found {fname} {lname}!!")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # --- FIND COURSES STUDENT IS IN ---
    elif student_choice == "Student Courses":
        st.write("### Find Courses a Student is in")
        input_option = st.pills("Input Option", ["ID", "Name"]) # allows user to input either ID or Name depending on what they have
        
        if input_option == "ID":
            studID = st.text_input("Enter Student's ID")

            if st.button("Find Student Courses"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT s.StudentID, s.Fname, s.Lname, c.CourseID, c.CourseName FROM STUDENT s LEFT JOIN ENROLLMENT e on s.StudentID = e.StudentID LEFT JOIN COURSE c on e.CourseID = c.CourseID WHERE s.StudentID = :1", [studID])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "CourseID", "Course_Name"])
                    cur.close()
                    conn.close()

                    if data:
                        st.table(df, hide_header=False)
                    else:
                        st.info("No records found.")
                except Exception as e:
                    st.error(f"Error: {e}")
        elif input_option == "Name":
            fname = st.text_input("Enter Student's First Name")
            lname = st.text_input("Enter Student's Last Name")

            if st.button("Find Student Courses"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT s.StudentID, s.Fname, s.Lname, c.CourseID, c.CourseName FROM STUDENT s LEFT JOIN ENROLLMENT e on s.StudentID = e.StudentID LEFT JOIN COURSE c on e.CourseID = c.CourseID WHERE s.Fname = :1 AND s.Lname = :2", [fname, lname])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "CourseID", "Course_Name"])
                    cur.close()
                    conn.close()

                    if data:
                        st.table(df, hide_header=False)
                    else:
                        st.info("No records found.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- FIND STUDENT'S GPA ---
    elif student_choice == "Student GPA":
        st.write("### Find Student's Current GPA")
        input_option = st.pills("Input Option", ["ID", "Name"]) # allows user to input either ID or Name depending on what they have
        
        if input_option == "ID":
            studID = st.text_input("Enter Student's ID")

            if st.button("Calculate GPA"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    # Update NAME where EMAIL matches
                    cur.execute("SELECT s.StudentID, s.Fname, s.Lname, ROUND(AVG(g.Grade), 2) as GPA FROM STUDENT s LEFT JOIN ENROLLMENT e on s.StudentID = e.StudentID LEFT JOIN GRADE g on e.EnrollmentID = g.EnrollmentID WHERE s.StudentID = :1 GROUP BY s.STUDENTID, s.FNAME, s.LNAME", [studID])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "GPA"])

                    if data:
                        st.table(df, hide_header= False)
                    else:
                        st.info("No records found.")

                except Exception as e:
                    st.error(f"Error: {e}")        
        elif input_option == "Name":
            fname = st.text_input("Enter Student's First Name")
            lname = st.text_input("Enter Student's Last Name")

            if st.button("Calculate GPA"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    # Update NAME where EMAIL matches
                    cur.execute("SELECT s.StudentID, s.Fname, s.Lname, ROUND(AVG(g.Grade), 2) as GPA FROM STUDENT s LEFT JOIN ENROLLMENT e on s.StudentID = e.StudentID LEFT JOIN GRADE g on e.EnrollmentID = g.EnrollmentID WHERE s.Fname = :1 AND s.Lname = :2 GROUP BY s.STUDENTID, s.FNAME, s.LNAME", [fname, lname])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "GPA"])

                    if data:
                        st.table(df, hide_header= False)
                    else:
                        st.info("No records found.")

                except Exception as e:
                    st.error(f"Error: {e}")

    # --- FIND STUDENT'S ATTENDANCE RATE FOR CURRENT CLASSES ---
    elif student_choice == "Student Attendance Rate":
        st.write("### Find Student Attendance Rate")
        input_option = st.pills("Input Option", ["ID", "Name"]) # allows user to input either ID or Name depending on what they have
        
        if input_option == "ID":
            studID = st.text_input("Enter Student's ID")

            if st.button("Find Attendance Rate"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    # Update NAME where EMAIL matches
                    cur.execute("SELECT s.StudentID, s.Fname, s.Lname, c.CourseName, a.AttendanceRate FROM STUDENT s LEFT JOIN ENROLLMENT e on s.StudentID = e.StudentID LEFT JOIN COURSE c on e.CourseID = c.CourseID LEFT JOIN ATTENDANCE a on e.EnrollmentID = a.EnrollmentID WHERE s.StudentID = :1", [studID])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "Course_Name", "Attendance_Rate"])

                    if data:
                        st.table(df, hide_header=False)
                    else:
                        st.info("No records found.")

                except Exception as e:
                    st.error(f"Error: {e}")
        elif input_option == "Name":
            fname = st.text_input("Enter Student's First Name")
            lname = st.text_input("Enter Student's Last Name")

            if st.button("Find Attendance Rate"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    # Update NAME where EMAIL matches
                    cur.execute("SELECT s.StudentID, s.Fname, s.Lname, c.CourseName, a.AttendanceRate FROM STUDENT s LEFT JOIN ENROLLMENT e on s.StudentID = e.StudentID LEFT JOIN COURSE c on e.CourseID = c.CourseID LEFT JOIN ATTENDANCE a on e.EnrollmentID = a.EnrollmentID WHERE s.Fname = :1 AND s.Lname = :2", [fname, lname])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["StudentID", "First_Name","Last_Name", "CourseName", "Attendance_Rate"])

                    if data:
                        st.table(df, hide_header=False)
                    else:
                        st.info("No records found.")

                except Exception as e:
                    st.error(f"Error: {e}")

# --- ALL COURSE RELATED QUERIES ---
elif bubble == "Course Information":

    # --- FIND COURSE INFORMATION ---
    if course_choice == "Find Course":
        st.write("### Find Information on a Course")
        input_option = st.pills("Input Option", ["ID", "Name"]) # allows user to input either ID or Name depending on what they have
        
        if input_option == "Name":
            cname = st.text_input("Enter a course name")

            if st.button("Find Course"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM Course c WHERE c.CourseName = :1", [cname])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["CourseID", "Course_Name", "Credits", "Description"])
                    conn.commit()
                    cur.close()
                    conn.close()
                    if data:
                        st.table(df, hide_header=False)
                        st.success(f"Successfully found {cname}!!")
                    else:
                        st.info("No records found.")
        
                except Exception as e:
                    st.error(f"Error: {e}")
        elif input_option == "ID":
            cid = st.text_input("Enter a Course ID")
            if st.button("Find Course"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM Course c WHERE c.CourseID = :1", [cid])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["CourseID", "Course_Name", "Credits", "Description"])
                    conn.commit()
                    cur.close()
                    conn.close()
                    if data:
                        st.table(df, hide_header=False)
                        st.success(f"Successfully found the course with the id {cid}!!")
                    else:
                        st.info("No records found.")
                    
                except Exception as e:
                    st.error(f"Error: {e}")

    # -- FIND TOTAL STUDENTS IN COURSE ---
    elif course_choice == "Course Enrollment Info":
        st.write("### Find total students in a course")
        input_option = st.pills("Input Option", ["ID", "Name"]) # allows user to input either ID or Name depending on what they have
        
        if input_option == "Name":
            cname = st.text_input("Enter a course name")
            if st.button("Find Enrollment Count"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT c.CourseID, c.CourseName, c.Credits, c.Description, COUNT(e.StudentID) AS StudentCount FROM Course c LEFT JOIN ENROLLMENT e on c.CourseID = e.COURSEID WHERE c.CourseName = :1 GROUP BY c.CourseID, c.CourseName, c.Credits, c.Description", [cname])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["CourseID", "Course_Name", "Credits", "Description", "Student_Count"])
                    conn.commit()
                    cur.close()
                    conn.close()
                    if data:
                        st.table(df, hide_header=False)
                    else:
                        st.info("No records found.")
                    st.success(f"Successfully found {cname}!!")
                except Exception as e:
                    st.error(f"Error: {e}")
        if input_option == "ID":
            cid = st.text_input("Enter a Course ID")
            if st.button("Find Enrollment Count"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT c.CourseID, c.CourseName, c.Credits, c.Description, COUNT(e.StudentID) AS StudentCount FROM Course c LEFT JOIN ENROLLMENT e on c.CourseID = e.COURSEID WHERE c.CourseID = :1 GROUP BY c.CourseID, c.CourseName, c.Credits, c.Description", [cid])
                    data = cur.fetchall()
                    df = pd.DataFrame(data, columns=["CourseID", "Course_Name", "Credits", "Description", "Student_Count"])
                    conn.commit()
                    cur.close()
                    conn.close()
                    if data:
                        st.table(df, hide_header=False)
                    else:
                        st.info("No records found.")
                    st.success(f"Successfully found the course with the ID {cid}!!")
                except Exception as e:
                    st.error(f"Error: {e}")

# run using: streamlit run app.py
