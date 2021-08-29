import pygsheets


service_file_path = "C:\\Users\\ivayl\\Documents\\Nexo Work\\google_api_key.json"


def write_to_gsheet(data):
    """
    Write a data frame on a google sheet
    """

    sheet = None
    # Authenticate
    creds = pygsheets.authorize(service_file=service_file_path)

    try:
        # Open the google sheet that updates the dashboard
        book = creds.open_by_key("1S8RC6zd7p7ZyxTJBSZs81DrF8Wk9Rx77-zJ_sgU4fzE")
        sheet = book.worksheet_by_title("Sheet1")

    except pygsheets.exceptions.SpreadsheetNotFound:
        print("Spreadsheet not found!")

    if sheet:
        # Clean the sheet and update the data
        sheet.clear()
        sheet.set_dataframe(data, (1, 1), encoding='utf-8', fit=True)
        sheet.frozen_rows = 1
