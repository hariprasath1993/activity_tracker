from notion_client import Client

notion = Client(auth="secret_ep0rkEuMC94NKTW9h5JUIhjqJ0C7y0Ef8DzUiFXFucZ")


class scheduled_meeting():
    MEETING_ACTIVITY_DB = "116609e67d7d8087a110e67e284e5292"

    def __init__(self, account_id) -> None:
        self.topic = ""
        self.account_id = account_id
        self.date = None
        self.time = None
        self.members = []
        self.customer_list = []
        self.meeting_minutes = ""
        self.action_item = ""
        self.is_presentation = False

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
                    "people": [{"id": user_id} for user_id in self.members]
                },
                "Company Presentation": {
                    "checkbox": self.is_presentation
                }
            }
        )
        self._add_meeting_minutes(new_page)

    def _add_meeting_minutes(self, new_page):
        notion.blocks.children.append(
            block_id=new_page['id'],  # Use the ID of the new page
            children=[
                {
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
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": self.meeting_minutes
                                }
                            }
                        ]
                    }
                },
                {
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
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": self.action_item
                                }
                            }
                        ]
                    }
                }
            ]
        )
