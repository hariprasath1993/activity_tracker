import streamlit as st

pages = {
    "Activity Trackers": [
        st.Page("activity_tracker.py", title="Track your daily activity"),
    ],
    "Reports": [
        st.Page("user_reports.py", title="User Reports"),
        st.Page("region_reports.py", title="Region Reports"),
    ],
    "Account Information": [
        st.Page("account_information.py", title="Account activity Tracker"),
    ],
}

pg = st.navigation(pages)
pg.run()
