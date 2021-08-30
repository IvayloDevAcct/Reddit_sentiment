import pygsheets

# This is the path to my token file. IT WON'T work on another machine. Please set the path to your token.
service_file_path = "C:\\Users\\ivayl\\Documents\\Nexo Work\\google_api_key.json"


workbook_id = "1S8RC6zd7p7ZyxTJBSZs81DrF8Wk9Rx77-zJ_sgU4fzE"
sheet_name = "Sheet1"


class GoogleSheet:
    def __init__(self, token, book_id, sheet_name):
        self.id = book_id
        self.__token = token
        self.sheet_name = sheet_name
        self.__sheet = self.get_sheet()

    def get_sheet(self):
        """Opens the sheet by it's ID"""

        sheet = None
        # Authenticate
        creds = pygsheets.authorize(service_file=self.__token)

        try:
            # Open the google sheet that updates the dashboard
            book = creds.open_by_key(self.id)
            sheet = book.worksheet_by_title(self.sheet_name)

        except pygsheets.exceptions.SpreadsheetNotFound:
            print("Spreadsheet not found!")

        return sheet

    def get_existing_post_ids(self):
        """Gets all existing post ids from the google sheet in order to avoid duplicates"""
        return self.__sheet.get_col(1)[1:]

    def add_data(self, data):
        """Adds the data to the googhe sheet"""
        self.__sheet.add_rows(1)
        self.__sheet.set_dataframe(data, (self.__sheet.rows, 1), encoding='utf-8', copy_head=False)

    def update_data(self, data):
        """Updates the rows in the google sheet that are present in the updated data list. Looks up by ID"""

        records = self.__sheet.get_all_records()

        # Start a counter (starting from row 2 to skip the headers)
        i = 2

        # Loop through all rows in the google sheet and see if any of the entries in the lists with post matches by ID
        for row in records:
            for post in data:
                if row["id"] == post["id"]:

                    new_values = [str(value) for value in post.values()][2:]

                    # Update the values of the row
                    self.__sheet.update_row(i, new_values, col_offset=2)

            # Increase the counter
            i += 1

