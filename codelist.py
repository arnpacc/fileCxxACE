import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

APP_CONFIG = {"request_timeout": 20,"max_retries": 5,"cache_duration": timedelta(minutes=30)}

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    pre_tag = soup.find("pre")
    if not pre_tag:
        return "Error: Missing pre tag"
    lines = pre_tag.get_text("\n").split("\n")
    now = datetime.now()
    for i in range(4, len(lines), 3):
        try:
            start_str, end_str = lines[i].strip().split(" - ")
            start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
            if start_time <= now <= end_time:
                code = lines[i+1].strip() if i+1 < len(lines) else ""
                return f"Valid Activation Code :\n\n{code}\n\nFrom: {start_str}\nTo:   {end_str}"
        except Exception:
            continue
    return "No valid code found"

def get_activation_code():
    url = "https://filecxx.com/en_US/activation_code.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    # در هر تلاش اطلاعاتی در مورد خطا چاپ می‌شود
    for attempt in range(APP_CONFIG["max_retries"]):
        try:
            print(f"\nAttempt {attempt+1} of {APP_CONFIG['max_retries']}.........\n")
            response = requests.get(url, headers=headers, timeout=APP_CONFIG["request_timeout"])
            response.raise_for_status()
            result = parse_html(response.text)
            return result
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
    return "Failed to connect after maximum retries."

if __name__ == "__main__":
    print("=================================")
    print("FileCXX Activation Code Extractor")
    print("=================================")
    result = get_activation_code()
    print(result)