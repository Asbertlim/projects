import streamlit as st
from supabase import create_client
from datetime import datetime, date

# ==========================================
# STUDY TRACKER
# ==========================================

st.set_page_config(
    page_title="Study Tracker",
    page_icon="📚",
    layout="centered"
)

# ==========================================
# SUPABASE CONNECTION
# ==========================================

if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = st.session_state.supabase

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_tasks():
    """Retrieve tasks allowed by the user's RLS policies."""
    response = (
        supabase.table("tasks")
        .select("id, name, priority, description, due_date, status")
        .order("id", desc=True)
        .execute()
    )
    return response.data or []


def format_date(value):
    """Display database dates as DD-MM-YY."""
    if not value:
        return "Not set"

    try:
        parsed = date.fromisoformat(str(value)[:10])
        return parsed.strftime("%d-%m-%y")
    except ValueError:
        return str(value)


def show_error(action, error):
    """Show an understandable error without exposing credentials."""
    st.error(f"{action} Please try again.")
    st.caption(f"Technical details: {type(error).__name__}")


def add_task(name, priority, description, due_date, status):
    """Add a task to the database."""
    task_data = {
        "name": name,
        "priority": int(priority),
        "description": description,
        "due_date": due_date.isoformat() if due_date else None,
        "status": status
    }

    # user_id is assigned by the database default auth.uid().
    # Never accept another user's ID from the form.
    supabase.table("tasks").insert(task_data).execute()


def delete_task(task_id):
    """Delete one task, subject to database security policies."""
    (
        supabase.table("tasks")
        .delete()
        .eq("id", task_id)
        .execute()
    )


def update_task_status(task_id, new_status):
    """Update a task's status, subject to database security policies."""
    (
        supabase.table("tasks")
        .update({"status": new_status})
        .eq("id", task_id)
        .execute()
    )


# ==========================================
# AUTHENTICATION
# ==========================================

st.title("📚 Study Tracker")
st.write(
    "Organize your studies, manage priorities, "
    "and keep track of your progress."
)

# This state is only a UI indicator. Database access is still
# controlled by Supabase authentication and RLS policies.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if not st.session_state.logged_in:

    st.divider()
    st.subheader("Welcome, Learner!")

    choice = st.radio(
        "Choose an option",
        ["Log in", "Create account"],
        horizontal=True
    )

    with st.form("auth_form"):
        email = st.text_input("Email address").strip()
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(
            choice,
            type="primary"
        )

    if submitted:
        if not email or not password:
            st.error("Please enter both your email and password.")

        elif choice == "Create account" and len(password) < 8:
            st.error("Please use a password with at least 8 characters.")

        else:
            try:
                if choice == "Create account":
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if response.session is not None:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.success(
                            "Registration submitted. Check your email "
                            "if confirmation is required, then log in."
                        )

                else:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if response.session is not None:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(
                            "No active session was returned. "
                            "Please try again."
                        )

            except Exception as error:
                show_error("Authentication failed.", error)

    st.stop()


# ==========================================
# SIGNED-IN APP
# ==========================================

st.caption(f"Signed in as {st.session_state.user_email}")

if st.button("Log out"):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.rerun()

st.divider()

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

# Fetch fresh data for each page.
try:
    tasks = get_tasks()
except Exception as error:
    show_error("Could not load your tasks.", error)
    st.stop()


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":
    st.header("📊 Your Dashboard")

    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks
        if task["status"] == "completed"
    )
    incomplete_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed_tasks)
    col3.metric("Incomplete", incomplete_tasks)

    st.divider()
    st.subheader("Your Current Tasks")

    if not tasks:
        st.info("You have no tasks yet. Select 'Add Task' to begin.")

    for task in tasks:
        with st.container(border=True):
            st.markdown(f"**{task['name'].title()}**")
            st.write(f"Priority: {task['priority']}")
            st.write(f"Due date: {format_date(task['due_date'])}")
            st.write(
                f"Description: {task.get('description') or 'None'}"
            )

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
            options=[1, 2, 3],
            format_func=lambda value: {
                1: "1 - High",
                2: "2 - Medium",
                3: "3 - Low"
            }[value]
        )

        description = st.text_area("Task description")

        has_due_date = st.checkbox("Set a due date")

        due_date = None
        if has_due_date:
            due_date = st.date_input(
                "Due date",
                value=date.today()
            )

        status = st.selectbox(
            "Task status",
            ["incomplete", "completed"],
            format_func=str.title
        )

        submitted = st.form_submit_button("Add Task")

    if submitted:
        if not name:
            st.error("Please enter a task name.")

        elif any(task["name"].lower() == name for task in tasks):
            st.error(
                "A task with this name already exists. "
                "Please choose another name."
            )

        else:
            try:
                add_task(
                    name,
                    priority,
                    description.strip(),
                    due_date,
                    status
                )
                st.success(f"Task '{name}' added successfully!")
                st.rerun()

            except Exception as error:
                show_error("Could not add the task.", error)


# ==========================================
# VIEW TASKS
# ==========================================

elif page == "View Tasks":
    st.header("📋 View Your Tasks")

    if not tasks:
        st.info("No tasks available. Add a task first.")

    for task in tasks:
        with st.expander(task["name"].title()):
            st.write(f"**Priority:** {task['priority']}")
            st.write(f"**Due date:** {format_date(task['due_date'])}")
            st.write(
                f"**Description:** {task.get('description') or 'None'}"
            )
            st.write(f"**Status:** {task['status'].title()}")


# ==========================================
# DELETE TASK
# ==========================================

elif page == "Delete Task":
    st.header("🗑️ Delete a Study Task")

    if not tasks:
        st.info("There are no tasks to delete.")

    else:
        selected_id = st.selectbox(
            "Select a task to delete",
            options=[task["id"] for task in tasks],
            format_func=lambda task_id: next(
                f"{task['name'].title()} (ID: {task_id})"
                for task in tasks
                if task["id"] == task_id
            )
        )

        selected_task = next(
            task for task in tasks
            if task["id"] == selected_id
        )

        confirm = st.checkbox(
            f"I confirm that I want to delete "
            f"'{selected_task['name']}'."
        )

        if st.button("Delete Task", type="primary"):
            if not confirm:
                st.warning("Please confirm before deleting the task.")

            else:
                try:
                    delete_task(selected_id)
                    st.success("Task deleted successfully.")
                    st.rerun()

                except Exception as error:
                    show_error("Could not delete the task.", error)


# ==========================================
# UPDATE TASK STATUS
# ==========================================

elif page == "Update Status":
    st.header("✅ Update Task Status")

    if not tasks:
        st.info("There are no tasks to update.")

    else:
        selected_id = st.selectbox(
            "Select a task",
            options=[task["id"] for task in tasks],
            format_func=lambda task_id: next(
                task["name"].title()
                for task in tasks
                if task["id"] == task_id
            )
        )

        selected_task = next(
            task for task in tasks
            if task["id"] == selected_id
        )

        current_status = selected_task["status"]

        new_status = st.selectbox(
            "Choose the new status",
            options=["incomplete", "completed"],
            index=1 if current_status == "completed" else 0,
            format_func=str.title
        )

        if st.button("Save Status"):
            try:
                update_task_status(selected_id, new_status)
                st.success("Task status updated successfully.")
                st.rerun()

            except Exception as error:
                show_error("Could not update the task.", error)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Study Tracker | Keep learning, one task at a time. 📖"
)
