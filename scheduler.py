import schedule
import time
import subprocess

def check():
    print("Search begin")
    subprocess.run(["python", "main.py"])

schedule.every(2).days.at("12:00").do(check)

