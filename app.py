import streamlit as st
import pandas as pd


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# SIMPLE CUSTOM STYLE
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7F8FC;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #1F2937;
    }

    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E5E7EB;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #6B7280;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# FUNCTIONS
# ==================================================

def check_score(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Very Good"
    elif score >= 60:
        return "Passed"
    else:
        return "Failed"


def class_result(average):
    if average >= 90:
        return "Excellent"
    elif average >= 75:
        return "Very Good"
    elif average >= 60:
        return "Passed"
    else:
        return "Needs Improvement"


# ==================================================
# SESSION STATE
# ==================================================

if "students" not in st.session_state:
    st.session_state.students = []


# ==================================================
# HEADER
# ==================================================

st.title("🎓 Student Performance Analyzer")

st.caption(
    "Add student scores and analyze overall class performance."
)

st.divider()


# ==================================================
# ADD STUDENT
# ==================================================

st.subheader("➕ Add Student")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

with col2:
    score = st.number_input(
        "Student Score",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )


if st.button("Add Student", type="primary"):

    if name.strip() == "":
        st.warning("Please enter the student's name.")

    else:
        result = check_score(score)

        student = {
            "Name": name.strip(),
            "Score": score,
            "Result": result
        }

        st.session_state.students.append(student)

        st.success(
            f"{name.strip()} added successfully — {result}"
        )


st.divider()


# ==================================================
# DASHBOARD
# ==================================================

if len(st.session_state.students) > 0:

    students = st.session_state.students

    # Create DataFrame
    df = pd.DataFrame(students)

    # ----------------------------------------------
    # CALCULATIONS
    # ----------------------------------------------

    total = 0

    for student in students:
        total += student["Score"]

    average = total / len(students)

    scores = []

    for student in students:
        scores.append(student["Score"])

    highest_score = max(scores)
    lowest_score = min(scores)

    passed_count = 0
    failed_count = 0

    for student in students:
        if student["Result"] == "Failed":
            failed_count += 1
        else:
            passed_count += 1

    pass_rate = (
        passed_count / len(students)
    ) * 100


    # ----------------------------------------------
    # FIND HIGHEST AND LOWEST STUDENTS
    # ----------------------------------------------

    highest_students = []
    lowest_students = []

    for student in students:

        if student["Score"] == highest_score:   
            highest_students.append(student["Name"])

        if student["Score"] == lowest_score:
            lowest_students.append(student["Name"])

    highest_names = ", ".join(highest_students)
    lowest_names = ", ".join(lowest_students)


    # ----------------------------------------------
    # CLASS OVERVIEW
    # ----------------------------------------------

    st.subheader("📊 Class Overview")

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            label="Total Students",
            value=len(students)
        )

    with metric2:
        st.metric(
            label="Average Score",
            value=f"{average:.1f}"
        )

    with metric3:
        st.metric(
            label="Pass Rate",
            value=f"{pass_rate:.1f}%"
        )

    with metric4:
        st.metric(
            label="Class Performance",
            value=class_result(average)
        )


    # ----------------------------------------------
    # PERFORMANCE HIGHLIGHTS
    # ----------------------------------------------

    st.subheader("🏆 Performance Highlights")

    highlight1, highlight2 = st.columns(2)

    with highlight1:
        st.metric(
            label=f"Highest Score — {highest_names}",
            value=highest_score
        )

    with highlight2:
        st.metric(
            label=f"Lowest Score — {lowest_names}",
            value=lowest_score
        )


    # ----------------------------------------------
    # RESULTS SUMMARY
    # ----------------------------------------------

    st.subheader("📈 Results Summary")

    result1, result2 = st.columns(2)

    with result1:
        st.metric(
            label="Passed Students",
            value=passed_count
        )

    with result2:
        st.metric(
            label="Failed Students",
            value=failed_count
        )


    # ----------------------------------------------
    # STUDENT TABLE
    # ----------------------------------------------

    st.subheader("📋 Student Records")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


    # ----------------------------------------------
    # SCORE CHART
    # ----------------------------------------------

    st.subheader("📊 Student Scores")

    chart_data = df.set_index("Name")[["Score"]]

    st.bar_chart(
        chart_data,
        height=350
    )


    # ----------------------------------------------
    # CLEAR DATA
    # ----------------------------------------------

    st.divider()

    if st.button("🗑️ Clear All Students"):

        st.session_state.students = []

        st.rerun()


# ==================================================
# EMPTY STATE
# ==================================================

else:

    st.info(
        "No students have been added yet. "
        "Add your first student to view the dashboard."
    )