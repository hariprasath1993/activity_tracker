from notion_client import Client
import datetime


ALL_ACCOUNTS_DB = "ecd2b7e64ce54b4ca278877c764c1519"


class Utils():
    ACCOUNT_INFO = {}

    @staticmethod
    def get_notion_client():
        notion = Client(
            auth="secret_ep0rkEuMC94NKTW9h5JUIhjqJ0C7y0Ef8DzUiFXFucZ")
        return notion

    @staticmethod
    def get_workspace_users():
        users = Utils.get_notion_client().users.list()  # Fetch all users in the workspace
        user_dict = {user['name']: user['id']
                     for user in users['results'] if user['type'] == 'person'}
        return user_dict

    @staticmethod
    def fetch_all_accounts():
        all_accounts = []
        has_more = True
        next_cursor = None

        while has_more:
            query_params = {
                "database_id": ALL_ACCOUNTS_DB,
                "page_size": 100  # Max page size
            }

            if next_cursor:
                query_params["start_cursor"] = next_cursor

            response = Utils.get_notion_client().databases.query(**query_params)

            # Append the fetched accounts
            all_accounts.extend(response['results'])

            # Check if there are more pages
            has_more = response.get('has_more', False)
            next_cursor = response.get('next_cursor')

        return all_accounts

    @staticmethod
    def get_account_names_and_ids():
        accounts = Utils.fetch_all_accounts()
        account_info = [
            {
                "name": page['properties']['Name']['title'][0]['plain_text'],
                "id": page['id']
            }
            for page in accounts
            # Ensure the 'Name' field exists
            if page['properties']['Name']['title']
        ]
        return account_info

    @staticmethod
    def get_account_names():
        if not Utils.ACCOUNT_INFO:
            Utils.ACCOUNT_INFO = Utils.get_account_names_and_ids()

        account_names = [account['name'] for account in Utils.ACCOUNT_INFO]
        return account_names

    @staticmethod
    def get_account_id_from_name(account_name):
        if not Utils.ACCOUNT_INFO:
            Utils.ACCOUNT_INFO = Utils.get_account_names_and_ids()
        return next(account['id'] for account in Utils.ACCOUNT_INFO if account['name']
                    == account_name)

    @staticmethod
    def check_for_time_validity(date):
        today = datetime.date.today()
        delta = today - date
        if delta.days > 1:
            return False
        return True
