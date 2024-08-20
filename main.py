import requests
from yay import Yay
import json
import random
import string
from time import sleep
from datetime import datetime
from colorama import Fore

API_BASE = "https://api.tempmail.lol"
PASSWORD = "329ywdgaodhwudd"

def get_temp_email():
    response = requests.get(f"{API_BASE}/generate")
    response.raise_for_status()
    data = response.json()
    return data['address'], data['token']

def get_verification_code(email_token):
    response = requests.get(f"{API_BASE}/auth/{email_token}")
    response.raise_for_status()
    data = response.json()
    for mail in data['email']:
        if "メールアドレスを認証してください" in mail['subject']:
             code = extract_code_from_email(mail['body'])
             return code
    return None

def extract_code_from_email(body):

    import re
    match = re.search(r'\b\d{6}\b', body)
    if match:
        return match.group(0)
    return None

while True:
    try:
        random_string = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 10))
        yay = Yay()
        
        email, email_token = get_temp_email()
        print(f"{Fore.CYAN}Generated email: {email}{Fore.RESET}")
        
        yay.register(email)
        sleep(30)
        
        code = get_verification_code(email_token)
        if not code:
            raise ValueError("Verification code not found in the email")
        
        token = yay.register_code(code=code, password=PASSWORD, nickname=random_string)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Fore.CYAN}{current_time} - Token: {token}{Fore.RESET}")
        sleep(100)
    except Exception as e:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Fore.CYAN}{current_time} - Error: {e}{Fore.RESET}")
        sleep(100)
        continue
