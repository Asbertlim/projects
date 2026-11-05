import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="EduPredict",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------
# 2. DATASET
# --------------------------------

data = {
    "study_hours": [2, 0, 3, 5, 6, 4, 6, 7, 8, 9, 3, 2, 2, 3, 1, 2, 1, 2, 2.5, 2, 0, 4, 3, 1, 3, 2, 2, 0, 3, 9, 4, 1, 3, 12, 4, 2, 1, 4, 0, 3, 0],

    "attendance": [40, 60, 50, 70, 90, 60, 85, 100, 80, 90, 80, 60, 50, 80, 50, 80, 100, 100, 90, 90, 100, 70, 45, 100, 85, 70, 85, 100, 90, 50, 80, 100, 90, 60, 65, 100, 70, 40, 100, 90, 100],

    "previous_scores": [40, 20, 35, 60, 90, 50, 70, 95, 90, 100, 65, 60, 60, 70, 60, 45, 50, 60, 70, 65, 80, 70, 60, 55, 70, 65, 80, 80, 85, 80, 75, 90, 60, 80, 75, 80, 100, 70, 90, 70, 100],

    "assignment": [0, 10, 20, 70, 100, 60, 80, 90, 100, 90, 70, 50, 60, 80, 40, 70, 65, 60, 85, 95, 80, 65, 60, 60, 90, 80, 90, 90, 75, 40, 85, 100, 100, 80, 90, 75, 70, 60, 100, 90, 100],

    "sleep_hours": [5, 3, 5, 6, 7, 5, 7, 6, 6, 5, 5, 4, 10, 7, 9, 6, 7, 5, 7, 8, 9, 6, 7, 8, 8, 6, 7, 8, 8, 4, 6, 8, 7, 2, 6, 8, 5, 6, 9, 8, 10],

    "results": [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0]
}

df = pd.DataFrame(data)

X = df[
    [
        "study_hours",
        "attendance",
        "previous_scores",
        "assignment",
        "sleep_hours"
    ]
]

y = df["results"]


# --------------------------------
# 3. TRAIN THE MODEL
# --------------------------------

@st.cache_resource
def train_model():

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y
    )

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    )

    model.fit(X_train, y_train)

    test_prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, test_prediction)

    report = classification_report(
        y_test,
        test_prediction,
        labels=[0, 1],
        target_names=["Low Performance", "High Performance"],
        zero_division=0
    )

    return model, accuracy, report


model, accuracy, report = train_model()


# --------------------------------
# 4. APP TITLE
# --------------------------------

st.title("🎓 EduPredict")

st.subheader("Student Performance Prediction")

st.write(
    "Enter the student's information below "
    "to receive a predicted performance category."
)

st.divider()


# --------------------------------
# 5. USER INPUT
# --------------------------------

st.header("Student Information")

with st.form("student_form"):

    user_study = st.number_input(
        "Daily study hours",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5
    )

    user_atd = st.number_input(
        "School attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=1.0
    )

    user_scr = st.number_input(
        "Previous average score (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0
    )

    user_asg = st.number_input(
        "Assignment completion (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=1.0
    )

    user_sleep = st.number_input(
        "Daily sleep hours",
        min_value=0.0,
        max_value=24.0,
        value=8.0,
        step=0.5
    )

    submitted = st.form_submit_button(
        "Predict Performance",
        use_container_width=True
    )


# --------------------------------
# 6. MAKE PREDICTION
# --------------------------------

if submitted:

    user_test = pd.DataFrame([{
        "study_hours": user_study,
        "attendance": user_atd,
        "previous_scores": user_scr,
        "assignment": user_asg,
        "sleep_hours": user_sleep
    }])

    prediction = model.predict(user_test)

    st.divider()
    st.header("Prediction Result")

    if prediction[0] == 0:

        st.warning(
            "Predicted category: Low Performance"
        )

    else:

        st.success(
            "Predicted category: High Performance"
        )

    st.caption(
        "This is an educational prediction based on "
        "a small synthetic dataset, not a reliable "
        "assessment of an actual student's ability."
    )


# --------------------------------
# 7. MODEL PERFORMANCE
# --------------------------------

with st.expander("View Model Performance"):

    st.metric(
        label="Model Accuracy",
        value=f"{accuracy:.2%}"
    )

    st.text("Classification Report:")

    st.code(report)
