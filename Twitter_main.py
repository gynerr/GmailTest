import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from dotenv import load_dotenv

load_dotenv()

class TwitterTest:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        chrome_options.add_argument("--new-window")
        chrome_options.add_argument("--no-restore-session")
        chrome_options.add_argument("--remote-debugging-port=9222")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.username = os.getenv("TWITTER_USERNAME")
        self.email = os.getenv("TWITTER_EMAIL")
        self.old_password = os.getenv("TWITTER_OLD_PASSWORD")
        self.new_password = os.getenv("TWITTER_NEW_PASSWORD")
        self.backup_email = os.getenv("TWITTER_BACKUP_EMAIL")
        self.twitter_url = "https://twitter.com/login"

    def login(self):
        self.driver.get(self.twitter_url)
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'))
        )
        username_input.send_keys(self.email)
        username_input.send_keys((Keys.ENTER))
        try:
            extra_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'))
            )
            extra_input.send_keys(self.username)
            extra_input.send_keys(Keys.ENTER)
        except:
            pass
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.send_keys(self.old_password)
        password_input.send_keys(Keys.ENTER)

    def change_password(self):
        self.driver.get("https://twitter.com/settings/password")
        current_password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "current_password"))
        )
        current_password_input.send_keys(self.old_password)

        new_password_input = self.driver.find_element(By.NAME, "new_password")
        new_password_input.send_keys(self.new_password)

        verify_password_input = self.driver.find_element(By.NAME, "password_confirmation")
        verify_password_input.send_keys(self.new_password)

        save_button = self.driver.find_element(By.XPATH,
                                                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[3]/button')
        save_button.click()


    def random_tweet(self):
        self.driver.get("https://twitter.com/compose/post")
        tweet_text = f"This is a random tweet {random.randint(1, 1000)}"
        tweet_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']")))
        tweet_input.send_keys(tweet_text)

        tweet_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]')
        tweet_button.click()

    def run_tests(self):
        self.login()
        time.sleep(6)
        self.change_password()
        self.random_tweet()
        self.driver.quit()


if __name__ == "__main__":
    twitter_test = TwitterTest()
    twitter_test.run_tests()