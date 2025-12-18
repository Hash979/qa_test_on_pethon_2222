from selenium.webdriver.common.by import By


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def logout(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "Logout").click()
        wd.implicitly_wait(1)
        wd.find_element(By.NAME, "username")

    def login(self, username, password):
        wd = self.app.wd
        wd.get("http://localhost/mantisbt-1.2.20/login_page.php")
        wd.find_element(By.NAME, "username").clear()
        wd.find_element(By.NAME, "username").send_keys(username)
        wd.find_element(By.NAME, "password").clear()
        wd.find_element(By.NAME, "password").send_keys(password)
        wd.find_element(By.XPATH, "//input[@value='Login']").click()

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements(By.XPATH, "//input[@value='Login']")) == 0

    def is_logged_in_as(self, username):
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element(
            By.CSS_SELECTOR,
            "td.login-info-left span.italic").text

    def ensure_login(self, username, password):
        self.app.open_home_page()
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)
