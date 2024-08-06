from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import os

load_dotenv()

class GoogleMailTest:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        chrome_options.add_argument("--new-window")  # Открытие нового окна
        chrome_options.add_argument("--no-restore-session")
        chrome_options.add_argument("--remote-debugging-port=9222")  # Включить режим отладки
        self.driver = webdriver.Chrome(options=chrome_options)
        self.email = os.getenv("GMAIL_EMAIL")
        self.old_password = os.getenv("GMAIL_OLD_PASSWORD")
        self.new_password = os.getenv("GMAIL_NEW_PASSWORD")
        self.first_name = os.getenv("GMAIL_FIRST_NAME")
        self.last_name = os.getenv("GMAIL_LAST_NAME")
        self.backup_email = os.getenv("GMAIL_BACKUP_EMAIL")
        self.gmail_url = "https://mail.google.com/"
        self.dob = ''

    def login(self):
        self.driver.get(self.gmail_url)
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "identifier"))
        )
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_input.send_keys(self.old_password)# Заменить на old_password!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        password_input.send_keys(Keys.ENTER)


    def change_password(self):
        self.driver.get("https://myaccount.google.com/security")

        password_change_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[4]/div/div/div[3]/div[2]/a'))
        )
        password_change_btn.click()
        new_password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        new_password_input.send_keys(self.new_password)

        confirm_password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "confirmation_password"))
        )
        confirm_password_input.send_keys(self.new_password)
        confirm_password_input.send_keys(Keys.ENTER)

    def change_name(self):
        self.driver.get("https://myaccount.google.com/personal-info")
        # time.sleep(1200)
        dob_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="i12"]/div/div[2]/div/div'))
        )
        self.dob = dob_element.text
        name_edit_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[2]/div/div/div[3]/div[2]/a'))
        )
        name_edit_btn.click()
        name_2_edit_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div[3]/div/div/ul/li[1]/div/div[2]/div/a'))
        )
        name_2_edit_btn.click()

        first_name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="i7"]'))
        )
        first_name_input.clear()
        first_name_input.send_keys(self.first_name)

        last_name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="i12"]'))
        )
        last_name_input.clear()
        last_name_input.send_keys(self.last_name)

        save_btn = self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div[2]/div/div/div[3]/div[2]/div/div/button')
        save_btn.click()


    def save_data_to_table(self):
        with open('gmail_user_data.csv', 'a') as file:
            file.write(
                f"{self.email},{self.new_password},{self.first_name},{self.last_name},{self.backup_email},{self.dob}\n")

    def run_tests(self):
        self.login()
        time.sleep(6)
        self.change_password()
        time.sleep(6)
        self.change_name()
        self.save_data_to_table()
        self.driver.quit()


if __name__ == "__main__":
    google_test = GoogleMailTest()
    google_test.run_tests()