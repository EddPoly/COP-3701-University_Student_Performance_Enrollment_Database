import pandas as pd
import numpy as np
from faker import Faker
import os

def email_from_name(fname, lname):
    return f"{fname[0]}{lname}@exampleemail.net".lower()

def letterGrade(grade):
    if grade >= 90:
        return 'A'
    elif grade >= 80:
        return 'B'
    elif grade >= 70:
        return 'C'
    elif grade >= 60:
        return 'D'
    else:
        return 'F'


fake = Faker("en_US")

input_file = "student_performance_updated_1000.csv"

df = pd.read_csv("student_performance_updated_1000.csv")
df = df.dropna()
df["StudentID"] = df["StudentID"].astype(str).str.split(r"\.").str[0]
df.to_csv("student_performance_df.csv", index=False)
df2 = pd.read_csv("UIUC_course_catalog.csv")

# Student
student_df = df[["StudentID"]].drop_duplicates().copy()
student_df["StudentID"] = student_df["StudentID"]
student_df["Fname"] = df["Name"].str.split().str[0]
student_df["Lname"] = df["Name"].str.split().str[-1]

# checking if there is a valid first name and last name
student_df = student_df[student_df["Fname"] != student_df["Lname"]]

# Using faker to generate additional student information
student_df["DOB"] = [fake.date_of_birth(minimum_age = 18, maximum_age = 30) for _ in range(len(student_df))]
student_df["Email"] = [email_from_name(f, l) for f, l in zip(student_df["Fname"], student_df["Lname"])]
student_df["Phone"] = [fake.numerify(text="###-###-####") for _ in range(len(student_df))]
student_df["AdmissionDate"] = [fake.date_between(start_date ="-6y", end_date = "-1y") for _ in range(len(student_df))]


student_df = student_df[["StudentID", "Fname", "Lname", "DOB", "Email", "Phone", "AdmissionDate"]]


# Course
df2 = df2.rename(columns={"Name": "CourseName"})
course_df = df2[["CourseName"]].drop_duplicates().copy()

# Isolating number from credit hours and getting rid of the 0s (from ranges of credit hours)
course_df["Credits"] = df2["Credit Hours"].str[0]
course_df = course_df[course_df["Credits"] != "0"]
course_df["Description"] = df2["Description"]

# assigning courseIDs for FK use
course_df["CourseID"] = [i + 1 for i in range(len(course_df))]


course_df = course_df[["CourseID", "CourseName", "Credits", "Description"]]


# Enrollment
enrollment_df = pd.DataFrame()
enrollment_df["EnrollmentID"] = [i for i in range(1, 3000)]

# FK random students and assign them random courses
enrollment_df["StudentID"] = np.random.choice(student_df["StudentID"], size=len(enrollment_df))
enrollment_df["CourseID"] = np.random.choice(course_df["CourseID"], size=len(enrollment_df))
enrollment_df = enrollment_df.drop_duplicates(subset=['StudentID', 'CourseID'])

# Enroll or waitlist students
status = ["Enrolled", "Enrolled", "Enrolled", "Enrolled", "Enrolled", "Enrolled", "Enrolled", "Waitlist"]
enrollment_df["Status"] = np.random.choice(status, size=len(enrollment_df))


enrollment_df = enrollment_df[["EnrollmentID", "StudentID", "CourseID", "Status"]]

# Grade
grade_df = pd.merge(df, enrollment_df, on="StudentID", how="inner")
grade_df = grade_df.drop_duplicates(subset=["EnrollmentID"])

# Random grades
grade_df["Grade"] = (grade_df["FinalGrade"] + np.random.randint(-10, 11, size=len(grade_df))).clip(0, 100)
grade_df["LetterGrade"] = [letterGrade(grade) for grade in grade_df["Grade"]]

# Waitlisted students should not have a grade (maybe should be NULL?)
grade_df = grade_df[grade_df["Status"] != "Waitlist"]

grade_df = grade_df[["EnrollmentID", "Grade", "LetterGrade"]]


# Attendance
attendance_df = pd.merge(df, enrollment_df, on="StudentID", how="inner")
attendance_df = attendance_df.drop_duplicates(subset=["EnrollmentID"])

attendance_df["AttendanceRate"] = (attendance_df["AttendanceRate"] + np.random.randint(-10, 11, size=len(attendance_df))).clip(0, 100)

# Waitlisted students have no class to attend (maybe should be NULL?)
attendance_df = attendance_df[attendance_df["Status"] != "Waitlist"]

attendance_df = attendance_df[["EnrollmentID", "AttendanceRate"]]


# Saving to csv
dir = os.getcwd()
student_df.to_csv(os.path.join(dir, "data", "student_information.csv"), index=False)
course_df.to_csv(os.path.join(dir, "data", "course_information.csv"), index=False)
enrollment_df.to_csv(os.path.join(dir, "data", "enrollment_information.csv"), index=False)
grade_df.to_csv(os.path.join(dir, "data", "grade_information.csv"), index=False)
attendance_df.to_csv(os.path.join(dir, "data", "attendance_information.csv"), index=False)
