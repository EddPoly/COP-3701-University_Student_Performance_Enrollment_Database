# COP-3701-University_Student_Performance_Enrollment_Database

## Tentative Project Scope
An academic database tracking students, courses, enrollment, grades, and attendance, with the goal to provide GPA calculation procedures, prerequisite enforcement triggers, and transcript generation queries.

## Users
University Administration

## Data Sources
Student Performance Predictions - https://www.kaggle.com/datasets/haseebindata/student-performance-predictions

University of Illinois Urbana-Champaign Course Catalog Dataset - https://discovery.cs.illinois.edu/dataset/course-catalog/

## Entity-Relationship Diagram
[Database ER Diagram](database_er.md)

## How to Use
Step 1: Use the create_db.sql file to create the database
Step 2: Use the dataload.py file with the provided data folder to load the data into the database. (Make sure to add your information to setup)
Step 3: Run app.py using your information to setup with the command:
  streamlit run app.py
