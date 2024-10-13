from utils.utils import Utils
import pandas as pd


class NotionDatabase():
    CALL_ACTIVITY_DB = "1743520fbefd4621aba92aedf7fe5ac3"
    MEETING_ACTIVITY_DB = "116609e67d7d8087a110e67e284e5292"

    @staticmethod
    def fetch_db_records_of_user(db, user):
        query = {
            "filter": {
                "property": "Members",  # Assuming 'account_id' is the property in the Notion DB
                "people": {
                    "contains": user
                }
            }
        }
        response = Utils.get_notion_client().databases.query(
            database_id=db, **query)
        return response.get("results", [])

    @staticmethod
    def get_call_activity_for_user(user_id):
        activities = []
        call_records = NotionDatabase.fetch_db_records_of_user(
            NotionDatabase.CALL_ACTIVITY_DB, user_id)
        for record in call_records:
            created_time = record['created_time']
            activities.append({
                "Activity": "Call",
                "created_time": created_time,
            })

        df = pd.DataFrame(activities)
        return df

    @staticmethod
    def get_meeting_activity_for_user(user_id):
        activities = []
        call_records = NotionDatabase.fetch_db_records_of_user(
            NotionDatabase.MEETING_ACTIVITY_DB, user_id)
        for record in call_records:
            created_time = record['created_time']
            activities.append({
                "Activity": "Meeting",
                "created_time": created_time,
            })

        df = pd.DataFrame(activities)
        return df
