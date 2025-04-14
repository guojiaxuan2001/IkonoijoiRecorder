import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

cred_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
client = gspread.authorize(creds)

sheet = client.open("Ikonoijoi").sheet1  
sheet.append_row(["account", "time", "text"]) 
