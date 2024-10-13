import streamlit as st
import requests
import datetime
from utils.callactivity import callactivity
from utils.scheduled_meeting import scheduled_meeting
from utils.utils import Utils
import time

st.title("Team Daily Activity Tracker")


if 'meeting_submitted' not in st.session_state:
    st.session_state.meeting_submitted = False


if 'follow_up_tasks' not in st.session_state:
    st.session_state.follow_up_tasks = []

if 'task_count' not in st.session_state:
    st.session_state.task_count = 0

if 'submitted_tasks' not in st.session_state:
    st.session_state.submitted_tasks = []


user_dict = Utils.get_workspace_users()

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        selected_users = st.multiselect("User", options=list(user_dict.keys()))
        selected_user_ids = [user_dict[user_name]
                             for user_name in selected_users]
        selected_account_name = st.selectbox(
            "Select an Account", Utils.get_account_names())
        selected_account_id = Utils.get_account_id_from_name(
            selected_account_name)
    with col2:
        date = st.date_input("Date", datetime.date.today())

activity_type = st.selectbox(
    "Activity Type", ['Call', 'Scheduled Meeting'])

with st.container():
    cold_calling = None

    if activity_type == 'Call':
        calling_activity = callactivity(selected_account_id)
        calling_activity.econ_participants = selected_user_ids
        calling_activity.date = date

        col1, col2 = st.columns(2)
        with col1:
            cold_calling = st.checkbox("Cold Call")
            if cold_calling:
                calling_activity.call_type = "Cold Call"
        with col2:
            calling_activity.is_successful = st.checkbox(
                'Customer picked the call')

        with st.form(key="call activity"):
            if calling_activity.is_successful:
                calling_activity.call_recording_link = st.text_input(
                    "Call Recording Link")

            # col1, col2 = st.columns(2)
            # with col1:
            #     calling_activity.date = st.date_input(
            #         "Call Attempt Date(Optional)", datetime.date.today())
            # with col2:
            #     calling_activity.time = st.time_input(
            #         "Call Attempt Time(optional)", datetime.time(18, 30))

            calling_activity.topic = st.text_input("Topic")
            calling_activity.call_interaction = st.text_area(
                "Explain the interaction")

            calling_activity.call_to_actions = st.multiselect("Call to Action", [
                'Scheduled a follow-up call', 'Pushed for Sample Purchase', 'Pushed for Sample Evaluation', 'Pushed for Stakeholder Meeting', 'Requested for Company Presentation'])

            call_submit = st.form_submit_button("Submit Call Activity")

            if call_submit:
                response = calling_activity.check_validity()
                if response == 'success':
                    if calling_activity.is_successful:
                        if not calling_activity.call_recording_link or not calling_activity.call_interaction:
                            st.error(
                                "Call recording link and interaction details are required for a successful call.")
                        else:
                            response = calling_activity.update_call_activity()
                            if response:
                                st.success("Activity logged successfully!")
                            else:
                                st.error("Error logging the activity.")

                    else:
                        response = calling_activity.update_call_activity()
                        if response:
                            st.success("Activity logged successfully!")
                        else:
                            st.error("Error connecting to notion")
                else:
                    st.error("Invalid response submitted - " + response)

    elif activity_type == "Mail":
        with st.form(key="mail activity"):
            mail_submit = st.form_submit_button("Submit Mail Activity")

    elif activity_type == "Scheduled Meeting":
        scheduled_meeting = scheduled_meeting(selected_account_id)
        scheduled_meeting.econ_participants = selected_user_ids
        scheduled_meeting.date = date
        with st.form(key="scheduled_meeting_activity"):

            scheduled_meeting.is_presentation = st.checkbox(
                'Is Presentation Meeting?')

            st.multiselect("Attendees", [])

            scheduled_meeting.topic = st.text_input("Topic")
            scheduled_meeting.meeting_minutes = st.text_area(
                "Meeting Minutes", placeholder="Elaborate the minutes in minimum 300 words")
            scheduled_meeting.action_item = st.text_area(
                "Action Items", placeholder="1. First item\n2. Second item\n3. Third item")
            scheduled_meeting_submit = st.form_submit_button(
                "Submit Meeting Activity")
            if scheduled_meeting_submit:
                st.session_state.meeting_submitted = True

                response = scheduled_meeting.check_validity()
                if response == 'success':
                    st.session_state.meeting_submitted = True
                    st.success("Meeting activity submitted successfully!")
                    scheduled_meeting._create_new_meeting_entry()
                else:
                    st.error(f'Error submitting the meeting - {response}')
