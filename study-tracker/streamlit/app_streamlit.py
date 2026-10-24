# IMPORTANT: This code is modified from the main code by cgpt.
# haven't deployed on streamlit yet.

import json
import os
from datetime import datetime
from supabase import create_client

import streamlit as st

# ==========================================
# STUDY TRACKER - STREAMLIT APP
# ==========================================

st.set_page_config(
    page_title="Study Tracker",
    page_icon="📚",
    layout="centered"
)
# Connect to Supabase for this user's app session
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

DATA_FILE = "tasks.json"


# ==========================================
# LOAD AND SAVE TASKS
# ==========================================

def load_tasks():
    """Load tasks from JSON, or return an empty dictionary."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

        except (json.JSONDecodeError, OSError):
            st.warning(
                "Could not read tasks.json. Starting with an empty task list."
            )

    return {}


def save_tasks():
    """Save current tasks to JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                st.session_state.tasks,
                file,
                indent=4,
                ensure_ascii=False
            )
        return True

    except OSError:
        st.error("Unable to save tasks. Please check file permissions.")
        return False


def normalize_task(task):
    """
    Support both the old list format and the new dictionary format.
    """
    if isinstance(task, dict):
        return {
            "priority": str(task.get("priority", "2")),
            "due_date": str(task.get("due_date", "")),
            "description": str(task.get("description", "")),
            "status": str(task.get("status", "incomplete")).lower()
        }

    if isinstance(task, list) and len(task) >= 4:
        # Convert the original format:
        # ["Priority: 1", "Due date: ...",
        #  "Description: ...", "Status : incomplete"]

        priority = str(task[0]).replace("Priority:", "").strip()
        due_date = str(task[1]).replace("Due date:", "").strip()
        description = str(task[2]).replace("Description:", "").strip()
        status = str(task[3]).replace("Status :", "").replace(
            "Status:", ""
        ).strip().lower()

        if status not in ("completed", "incomplete"):
            status = "incomplete"

        return {
            "priority": priority,
            "due_date": due_date,
            "description": description,
            "status": status
        }

    return None


# Initialize tasks once per user session.
if "tasks" not in st.session_state:
    raw_tasks = load_tasks()
    st.session_state.tasks = {}

    for name, task in raw_tasks.items():
        normalized = normalize_task(task)

        if normalized is not None:
            st.session_state.tasks[name] = normalized


# ==========================================
# APP HEADER
# ==========================================

st.title("📚 Study Tracker")
st.subheader("Welcome, Learner!")

st.write(
    "Organize your studies, manage priorities, "
    "and keep track of your progress."
)

st.divider()


# ==========================================
# NAVIGATION
# ==========================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Task",
        "View Tasks",
        "Delete Task",
        "Update Status"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":
    tasks = st.session_state.tasks

    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks.values()
        if task["status"] == "completed"
    )
    incomplete_tasks = total_tasks - completed_tasks

    st.header("Your Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed_tasks)
    col3.metric("Incomplete", incomplete_tasks)

    st.divider()

    if not tasks:
        st.info("You have no tasks yet. Select 'Add Task' to get started.")
    else:
        st.write("### Your Current Tasks")

        for name, task in tasks.items():
            with st.container(border=True):
                st.markdown(f"**{name}**")

                st.write(f"Priority: {task['priority']}")
                st.write(f"Due date: {task['due_date']}")
                st.write(f"Description: {task['description']}")

                if task["status"] == "completed":
                    st.success("Status: Completed")
                else:
                    st.warning("Status: Incomplete")


# ==========================================
# ADD TASK
# ==========================================

elif page == "Add Task":
    st.header("➕ Add a Study Task")

    with st.form("add_task_form"):
        name = st.text_input("Task name").strip().lower()

        priority = st.selectbox(
            "Priority level",
            options=["1", "2", "3"],
            format_func=lambda value: {
                "1": "1 - High",
                "2": "2 - Medium",
                "3": "3 - Low"
            }[value]
        )

        description = st.text_area("Task description")

        due_date = st.text_input(
            "Due date (DD-MM-YY)",
            placeholder="For example: 25-12-26"
        ).strip()

        status = st.selectbox(
            "Task status",
            ["incomplete", "completed"]
        )

        submitted = st.form_submit_button("Add Task")

    if submitted:
        if not name:
            st.error("Please enter a task name.")

        elif name in st.session_state.tasks:
            st.error(
                "A task with this name already exists. "
                "Please choose another name."
            )

        elif due_date:
            try:
                datetime.strptime(due_date, "%d-%m-%y")
            except ValueError:
                st.error("Please enter the date in DD-MM-YY format.")
                st.stop()

            st.session_state.tasks[name] = {
                "priority": priority,
                "due_date": due_date,
                "description": description,
                "status": status
            }

            if save_tasks():
                st.success(f"Task '{name}' added successfully!")

        else:
            st.session_state.tasks[name] = {
                "priority": priority,
                "due_date": "",
                "description": description,
                "status": status
            }

            if save_tasks():
                st.success(f"Task '{name}' added successfully!")


# ==========================================
# VIEW TASKS
# ==========================================

elif page == "View Tasks":
    st.header("📋 View Your Tasks")

    tasks = st.session_state.tasks

    if not tasks:
        st.info("No tasks available. Add a task first.")

    else:
        for name, task in tasks.items():
            with st.expander(name.title()):
                st.write(f"**Priority:** {task['priority']}")
                st.write(f"**Due date:** {task['due_date'] or 'Not set'}")
                st.write(f"**Description:** {task['description'] or 'None'}")
                st.write(f"**Status:** {task['status'].title()}")


# ==========================================
# DELETE TASK
# ==========================================

elif page == "Delete Task":
    st.header("🗑️ Delete a Study Task")

    tasks = st.session_state.tasks

    if not tasks:
        st.info("There are no tasks to delete.")

    else:
        selected_task = st.selectbox(
            "Select a task to delete",
            options=list(tasks.keys()),
            format_func=lambda name: name.title()
        )

        confirm = st.checkbox(
            f"I confirm that I want to delete '{selected_task}'."
        )

        if st.button("Delete Task", type="primary"):
            if confirm:
                del st.session_state.tasks[selected_task]

                if save_tasks():
                    st.success(f"Task '{selected_task}' deleted.")
                    st.rerun()
            else:
                st.warning("Please confirm before deleting the task.")


# ==========================================
# UPDATE TASK STATUS
# ==========================================

elif page == "Update Status":
    st.header("✅ Update Task Status")

    tasks = st.session_state.tasks

    if not tasks:
        st.info("There are no tasks to update.")

    else:
        selected_task = st.selectbox(
            "Select a task",
            options=list(tasks.keys()),
            format_func=lambda name: name.title()
        )

        current_status = tasks[selected_task]["status"]

        new_status = st.selectbox(
            "Choose the new status",
            options=["incomplete", "completed"],
            index=(
                1 if current_status == "completed" else 0
            ),
            format_func=lambda value: value.title()
        )

        if st.button("Save Status"):
            st.session_state.tasks[selected_task]["status"] = new_status

            if save_tasks():
                st.success(
                    f"'{selected_task}' is now marked as {new_status}."
                )
                st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Study Tracker | Keep learning, one task at a time. 📖"
)
