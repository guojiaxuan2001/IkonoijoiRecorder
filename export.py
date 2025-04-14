import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("capable-sled-456409-b6-8f3c678b6683.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Ikonoijoi").sheet1  
sheet.append_row(["account", "time", "text"])  