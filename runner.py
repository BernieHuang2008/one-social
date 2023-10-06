"""
Post article on a specified platform with their config file
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
import json


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
        with open(f"platforms/{config_file.lower()}.json", 'r') as f:
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
        self.driver.find_element(
            By.CSS_SELECTOR, config['title']).send_keys(content['title'])
        self.driver.find_element(
            By.CSS_SELECTOR, config['author']).send_keys(content['author'])
        self.driver.find_element(
            By.CSS_SELECTOR, config['content']).send_keys(content['content'])
        print("\033[90m [+] Content wrote successfully. \033[0m")

    def main(self, post_type, content):
        # init
        self.get_config('wechat')
        self.open_driver()

        # login
        self.login()

        # navigate to post page
        self.navigate_to(self.config['post'][post_type]['nav'])

        # write content
        self.write_content(self.config['post'][post_type], content)


if __name__ == '__main__':
    runner = Runner()
    runner.main('general', {
                    'title': 'this is title',
                    'author': 'i author',
                    'content': 'test content (only text content is available now)'
                })
    import time
    time.sleep(120)
