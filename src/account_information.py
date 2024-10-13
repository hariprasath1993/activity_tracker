import plotly.express as px
import streamlit as st
from notion_client import Client
import pandas as pd
from utils.utils import Utils
from utils.database import NotionDatabase
import calplot
import matplotlib.pyplot as plt


def fetch_db_items(database_id, account_id):
    query = {
        "filter": {
            "property": "Account",
            "relation": {
                "contains": account_id
            }
        }
    }
    response = Utils.get_notion_client().databases.query(
        database_id=database_id, **query)
    return response.get("results", [])

# Combine records from two databases


def get_combined_records(db1_id, db2_id, account_id):
    activities = []
    call_records = fetch_db_items(db1_id, account_id)
    for record in call_records:
        activity = record['properties']['Name']['title'][0]['plain_text'] if record['properties']['Name']['title'] else ""

        created_time = record['created_time']

        content = record['properties']['Meeting Minutes']['rich_text'][0][
            'plain_text'] if record['properties']['Meeting Minutes']['rich_text'] else ""

        activities.append({
            "Activity": "📞",
            "Subject": activity,
            "created_time": created_time,
            "Minutes": content
        })

    df = pd.DataFrame(activities)
    # if df is not None:
    #     df['created_time'] = pd.to_datetime(df['created_time'])
    #     df = df.sort_values(by='created_time', ascending=True)

    return df


st.title("Account Activity Timeline")
account_name = st.selectbox("Select an account", Utils.get_account_names())
account_id = Utils.get_account_id_from_name(account_name)


if account_id:
    combined_records = get_combined_records(
        NotionDatabase.CALL_ACTIVITY_DB, NotionDatabase.MEETING_ACTIVITY_DB, account_id)

    if not combined_records.empty:
        combined_records['created_time'] = pd.to_datetime(
            combined_records['created_time'])
        combined_records['date'] = combined_records['created_time'].dt.date
        activity_counts = combined_records.groupby('date').size()
        activity_counts.index = pd.to_datetime(activity_counts.index)
        fig, ax = calplot.calplot(activity_counts, cmap='Blues', vmin=0)
        st.pyplot(fig)

        # decorating final dataframe
        combined_records = combined_records.set_index('date').drop(
            columns=['created_time']).sort_index(ascending=False)
        st.dataframe(combined_records)
    else:
        st.write("No records found for this Account ID.")
