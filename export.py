import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("capable-sled-456409-b6-8f3c678b6683.json", scope)
client = gspread.authorize(creds)


cred_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
client = gspread.authorize(creds)

sheet = client.open("Ikonoijoi").sheet1  
sheet.append_row(["account", "time", "text"]) 
