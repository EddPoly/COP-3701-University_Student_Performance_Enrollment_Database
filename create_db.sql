CREATE TABLE Student(
    StudentID NUMBER PRIMARY KEY,
    Fname varchar(20) NOT NULL,
    Lname varchar(20) NOT NULL,
    DOB DATE NOT NULL,
    Email varchar(50) NOT NULL,
    Phone varchar(14),
    AdmissionDate DATE NOT NULL
);

CREATE TABLE Course(
    CourseID NUMBER PRIMARY KEY,
    CourseName varchar(100) NOT NULL,
    Credits NUMBER NOT NULL,
    Description varchar(3000)
);

CREATE TABLE Enrollment(
    EnrollmentID NUMBER PRIMARY KEY,
    StudentID NUMBER NOT NULL,
    CourseID NUMBER NOT NULL,
    Status varchar(8) NOT NULL
);

ALTER TABLE Enrollment
ADD CONSTRAINT FK_StudentID
FOREIGN KEY (StudentID)
REFERENCES Student(StudentID);

ALTER TABLE Enrollment
ADD CONSTRAINT FK_CourseID
FOREIGN KEY (CourseID)
REFERENCES Course(CourseID);

ALTER TABLE Enrollment
ADD CONSTRAINT UK_Student_Course UNIQUE (StudentID, CourseID);

CREATE TABLE Grade(
    EnrollmentID NUMBER PRIMARY KEY,
    Grade NUMBER NOT NULL,
    LetterGrade varchar(1) NOT NULL
);

ALTER TABLE Grade
ADD CONSTRAINT FK_Grade_EnrollmentID
FOREIGN KEY (EnrollmentID)
REFERENCES Enrollment(EnrollmentID);

CREATE TABLE Attendance(
    EnrollmentID NUMBER PRIMARY KEY,
    AttendanceRate NUMBER NOT NULL
);

ALTER TABLE Attendance
ADD CONSTRAINT FK_Attendance_EnrollmentID
FOREIGN KEY (EnrollmentID)
REFERENCES Enrollment(EnrollmentID);

COMMIT;
