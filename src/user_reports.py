import streamlit as st
import pandas as pd
from utils.utils import Utils
import plotly.express as px
from utils.database import NotionDatabase


def filter_last_2_day_activities():
    if not total_activities.empty:
        total_activities['created_time'] = pd.to_datetime(
            total_activities['created_time'])
        today = pd.Timestamp.now(tz='UTC')
        last_2_days = today - pd.Timedelta(days=2)
        filtered_df = total_activities[total_activities['created_time'] >= last_2_days]
        activity_counts = filtered_df['Activity'].value_counts().reset_index()
        activity_counts.columns = ['Activity', 'Count']
        fig = px.bar(activity_counts, x='Activity', y='Count', color='Activity',
                     title="Activity Counts for the Last 2 Days")
        st.plotly_chart(fig)


def filter_last_n_day_activities(n):
    if not total_activities.empty:
        total_activities['created_time'] = pd.to_datetime(
            total_activities['created_time'])
        today = pd.Timestamp.now(tz='UTC')
        last_n_days = today - pd.Timedelta(days=n)

        filtered_df = total_activities[total_activities['created_time'] >= last_n_days]

        filtered_df['created_date'] = filtered_df['created_time'].dt.date
        activity_counts = filtered_df.groupby(
            ['created_date', 'Activity']).size().unstack(fill_value=0)

        st.line_chart(activity_counts)


st.header('User Activity Report')
selected_user = st.selectbox("Select User", Utils.get_workspace_users())
daily, weekly, monthly = st.tabs(['Last 2 Days', 'Weekly', 'Monthly'])
call_activity = NotionDatabase.get_call_activity_for_user(
    Utils.get_user_id_from_name(selected_user))
meeting_activity = NotionDatabase.get_meeting_activity_for_user(
    Utils.get_user_id_from_name(selected_user))
total_activities = pd.concat(
    [call_activity, meeting_activity], ignore_index=True)


with daily:
    filter_last_2_day_activities()
with weekly:
    filter_last_n_day_activities(7)
with monthly:
    filter_last_n_day_activities(30)
