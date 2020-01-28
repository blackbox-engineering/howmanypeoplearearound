import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


class GSheet:
    """
    Class that just handles writing to a Google Sheet.
    The class expects the google sheet to already exist, and have
    the correct permissions set in order to access it.

    Follow the gspread documentation in order to obtain credentials:
     - https://gspread.readthedocs.io/en/latest/oauth2.html#using-signed-credentials
    """

    def __init__(self, creds_file, sheet_title, sheet_headers):
        self.title = sheet_title
        self.headers = sheet_headers

        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, SCOPE)
        self.google_client = gspread.authorize(credentials)

        self.google_worksheet = self.google_client.open(self.title).sheet1
        self.write_header_if_first_row_in_sheet()

    def write_header_if_first_row_in_sheet(self):
        if not self.google_worksheet.row_values(1):
            self.google_worksheet.append_row(self.headers)

    def append_row(self, row):
        self.google_worksheet.append_row(row)
