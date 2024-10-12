from notion_client import Client
from utils.utils import Utils

notion = Client(auth="secret_ep0rkEuMC94NKTW9h5JUIhjqJ0C7y0Ef8DzUiFXFucZ")


class callactivity():
    CALL_ACTIVITY_DB = "1743520fbefd4621aba92aedf7fe5ac3"

    def __init__(self, account_id) -> None:
        self.account_id = account_id
        self.topic = ""
        self.is_successful = False
        self.call_type = 'Follow Up'
        self.date = None
        self.time = None
        self.call_interaction = ""
        self.call_to_actions = []
        self.call_recording_link = None
        self.econ_participants = None
        self.customer_participants = None

    def check_validity(self):
        if not self.econ_participants:
            return "No users selected"
        if self.topic == '':
            return "Topic cannot be empty"
        if len(self.call_interaction.split()) < 2:
            return "Minutes are less than 300 words"
        if self.call_to_actions == []:
            return "Call to action cannot be empty"
        if not Utils.check_for_time_validity(self.date):
            return 'You cannot log activities for dates more than 1 day in the past.'

        return 'success'

    def update_call_activity(self):
        data = {
            "parent": {"database_id": callactivity.CALL_ACTIVITY_DB},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                    "content": self.topic
                            }
                        }
                    ]
                },
                "Members": {
                    "people": [{"id": user_id} for user_id in self.econ_participants]
                },
                "Account": {
                    "relation": [
                        {"id": self.account_id}
                    ]
                },
                "Call Type": {
                    "select": {"name": self.call_type}
                },
                "Customer Picked": {
                    "checkbox": self.is_successful
                },
                "Freshcaller Link": {
                    "url": self.call_recording_link
                },
                "Meeting Minutes": {  # The name of your text field property
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                    "content": self.call_interaction
                            }
                        }
                    ]
                },
                "Call to Action": {
                    "multi_select": [{"name": action} for action in self.call_to_actions]
                }
            }
        }

        return notion.pages.create(**data)
