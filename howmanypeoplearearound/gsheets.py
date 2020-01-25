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
        self.gc = gspread.authorize(credentials)

        self.wks = self.gc.open(self.title).sheet1
        self._check_header()

    def _check_header(self):
        if not self.wks.row_values(1):
            self.wks.append_row(self.headers)

    def append_row(self, row):
        self.wks.append_row(row)
