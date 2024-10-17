from notion_client import Client
from utils.utils import Utils


notion = Client(auth="secret_ep0rkEuMC94NKTW9h5JUIhjqJ0C7y0Ef8DzUiFXFucZ")


class scheduled_meeting():
    MEETING_ACTIVITY_DB = "116609e67d7d8087a110e67e284e5292"
    MIN_WORD_COUNT = 2

    def __init__(self, account_id) -> None:
        self.topic = ""
        self.account_id = account_id
        self.date = None
        self.time = None
        self.econ_participants = []
        self.customer_list = []
        self.meeting_minutes = ""
        self.action_item = ""
        self.is_presentation = False

    def check_validity(self):
        if not self.econ_participants:
            return "No users selected"
        if self.topic == '':
            return "Topic cannot be empty"
        if len(self.meeting_minutes.split()) < scheduled_meeting.MIN_WORD_COUNT:
            return "Minutes are less than 300 words"
        if len(self.action_item.split()) < scheduled_meeting.MIN_WORD_COUNT:
            return "Action Item cannot be empty"
        if not Utils.check_for_time_validity(self.date):
            return 'You cannot log activities for dates more than 1 day in the past.'

        return 'success'

    def _create_new_meeting_entry(self):
        new_page = notion.pages.create(
            parent={"database_id": scheduled_meeting.MEETING_ACTIVITY_DB},
            properties={
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
                "Account": {
                    "relation": [
                        {"id": self.account_id}
                    ]
                },
                "Members": {
                    "people": [{"id": user_id} for user_id in self.econ_participants]
                },
                "Company Presentation": {
                    "checkbox": self.is_presentation
                }
            }
        )
        self._add_meeting_minutes(new_page)

    def _add_meeting_minutes(self, new_page):
        def chunk_text(text, chunk_size=2000):
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        # Break meeting minutes and action items into chunks
        meeting_minutes_chunks = chunk_text(self.meeting_minutes)
        action_item_chunks = chunk_text(self.action_item)

        children_blocks = []

        # Add heading for Meeting Minutes
        children_blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Meeting Minutes"
                        }
                    }
                ]
            }
        })

        # Add Meeting Minutes content in chunks
        for chunk in meeting_minutes_chunks:
            children_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                    ]
                }
            })

        # Add heading for Action Items
        children_blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Action Items"
                        }
                    }
                ]
            }
        })

        # Add Action Items content in chunks
        for chunk in action_item_chunks:
            children_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                    ]
                }
            })

        # Append all children blocks to the page
        notion.blocks.children.append(
            block_id=new_page['id'],  # Use the ID of the new page
            children=children_blocks
        )
