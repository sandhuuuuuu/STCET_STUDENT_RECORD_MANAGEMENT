import streamlit as st
import sqlite3
import pandas as pd

# ------------------------------
# Database Connection
# ------------------------------

conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
gender TEXT,
course TEXT,
email TEXT,
phone TEXT
)
""")
conn.commit()

# ------------------------------
# Functions
# ------------------------------

def add_student(name, age, gender, course, email, phone):
    cursor.execute("""
    INSERT INTO students(name,age,gender,course,email,phone)
    VALUES(?,?,?,?,?,?)
    """, (name, age, gender, course, email, phone))
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return data


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


def update_student(student_id, name, age, gender, course, email, phone):
    cursor.execute("""
    UPDATE students
    SET
    name=?,
    age=?,
    gender=?,
    course=?,
    email=?,
    phone=?
    WHERE id=?
    """, (name, age, gender, course, email, phone, student_id))
    conn.commit()


def get_student(student_id):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    return cursor.fetchone()


# ------------------------------
# Streamlit Page
# ------------------------------

st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student"
]

choice = st.sidebar.selectbox("Menu", menu)

# ------------------------------
# HOME
# ------------------------------

if choice == "Home":

    st.subheader("Dashboard")

    students = view_students()

    st.metric("Total Students", len(students))

    st.write("""
This project demonstrates:

- Streamlit
- SQLite Database
- SQL CRUD Operations
- Deployable on Streamlit Community Cloud
""")

# ------------------------------
# ADD
# ------------------------------

elif choice == "Add Student":

    st.subheader("Add Student")

    name = st.text_input("Student Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        step=1
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    course = st.text_input("Course")

    email = st.text_input("Email")

    phone = st.text_input("Phone")

    if st.button("Add Student"):

        add_student(
            name,
            age,
            gender,
            course,
            email,
            phone
        )

        st.success("Student Added Successfully!")

# ------------------------------
# VIEW
# ------------------------------

elif choice == "View Students":

    st.subheader("Student Records")

    data = view_students()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Course",
            "Email",
            "Phone"
        ]
    )

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

# ------------------------------
# UPDATE
# ------------------------------

elif choice == "Update Student":

    st.subheader("Update Student")

    data = view_students()

    ids = [i[0] for i in data]

    if len(ids) == 0:
        st.warning("No student records found.")

    else:

        selected = st.selectbox(
            "Select Student ID",
            ids
        )

        student = get_student(selected)

        name = st.text_input(
            "Name",
            student[1]
        )

        age = st.number_input(
            "Age",
            value=student[2]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(student[3])
        )

        course = st.text_input(
            "Course",
            student[4]
        )

        email = st.text_input(
            "Email",
            student[5]
        )

        phone = st.text_input(
            "Phone",
            student[6]
        )

        if st.button("Update"):

            update_student(
                selected,
                name,
                age,
                gender,
                course,
                email,
                phone
            )

            st.success("Student Updated Successfully!")

# ------------------------------
# DELETE
# ------------------------------

elif choice == "Delete Student":

    st.subheader("Delete Student")

    data = view_students()

    ids = [i[0] for i in data]

    if len(ids) == 0:
        st.warning("No student records available.")

    else:

        selected = st.selectbox(
            "Select Student ID",
            ids
        )

        student = get_student(selected)

        st.write(student)

        if st.button("Delete Student"):

            delete_student(selected)

            st.success("Student Deleted Successfully!")
