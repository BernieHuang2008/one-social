"""
Post article on a specified platform with their config file
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver as webdriver
import json
import os
import media


GLOBAL_CONFIG = {
    "selenium_driver": "edge",
}


class Runner:
    def open_driver(self):
        driver_name = GLOBAL_CONFIG['selenium_driver'].lower()

        if driver_name == 'edge':
            driver = webdriver.Edge()
        elif driver_name == 'chrome':
            driver = webdriver.Chrome()
        elif driver_name == 'firefox':
            driver = webdriver.Firefox()
        else:
            raise Exception(f"Unknown driver: {driver_name}")

        driver.get(self.config['base_url'])

        self.driver = driver

    def get_config(self, config_file):
        """
        Get config from config file
        """
        with open(f"social_platforms/{config_file.lower()}.json", 'r') as f:
            config = json.load(f)
        self.config = config

    def login(self):
        # login methods
        def login_pwd(username, password):
            self.driver.find_element(
                By.CSS_SELECTOR, self.config['login_username']).send_keys(username)
            self.driver.find_element(
                By.CSS_SELECTOR, self.config['login_password']).send_keys(password)
            self.driver.find_element(
                By.CSS_SELECTOR, self.config['login_submit']).click()

        def login_qrcode():
            print(
                "\033[31m [!] Please scan the QR code to login. (You have 60s to complete this step ...) \033[0m")

            # wait for login
            wait = WebDriverWait(self.driver, 60)
            current_url = self.driver.current_url
            wait.until(EC.url_changes(current_url))

            print("\033[90m [+] Login successfully. \033[0m")

        # login auto-switcher
        if self.config['login']['type'] == 'qrcode':
            login_qrcode()

    def navigate_to(self, nav):
        """
        Navigate to a specified page with a list of commands
        """
        for command, para in nav['steps']:
            if command == 'c':
                self.driver.find_element(By.CSS_SELECTOR, para).click()
            if command == 's':
                self.driver.switch_to.window(self.driver.window_handles[para])

        # wait for page loaded
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, nav['checker'])))

    def write_content(self, config, content):
        """
        Write content to a specified platform
        """
        # write title & author
        self.driver.find_element(
            By.CSS_SELECTOR, config['title']).send_keys(content['title'])
        self.driver.find_element(
            By.CSS_SELECTOR, config['author']).send_keys(content['author'])

        # write content
        target = self.driver.find_element(By.CSS_SELECTOR, config['content'])
        for item in content['content']:
            if isinstance(item, str):  # text content
                target.send_keys(item)
            elif isinstance(item, media.Image):  # media.image content
                item.copy_to_clipboard()
                target.send_keys(Keys.CONTROL,'v')
            else:
                raise Exception(f"Unknown content type: {type(item)}")

        # print log
        print("\033[90m [+] Content wrote successfully. \033[0m")

    def main(self, social_platform, post_type, content):
        # init
        self.get_config(social_platform)
        self.open_driver()

        # login
        try_again = True
        while try_again:
            if os.path.exists(f"cookies/{social_platform}.json"):
                with open(f"cookies/{social_platform}.json", 'r') as f:
                    cookies = json.load(f)

                for cookie in cookies:
                    self.driver.add_cookie(cookie)

                self.driver.refresh()

                # check success
            else:
                self.login()
                cookies = self.driver.get_cookies()
                with open(f"cookies/{social_platform}.json", 'w') as f:
                    json.dump(cookies, f)

            # check status
            try:
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.config['login']['checker'])))
                print("\033[90m [+] Login successfully. \033[0m")
                try_again = False
            except:
                print("\033[31m [!] Login failed. Please try again. \033[0m")
                os.delete(f"cookies/{social_platform}.json")
                try_again = True

        # navigate to post page
        self.navigate_to(self.config['post'][post_type]['nav'])

        # write content
        self.write_content(self.config['post'][post_type], content)


if __name__ == '__main__':
    runner = Runner()
    runner.main('wechat', 'general', {
        'title': 'this is title',
        'author': 'i author',
        'content': [
            'test content (only text content is available now)\nnew line. ',
            media.Image('C:/Users/BernieHuang/Pictures/diary.png')
        ]
    })
    import time
    time.sleep(120)
