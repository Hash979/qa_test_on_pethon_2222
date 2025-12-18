from selenium import webdriver
from fixture.session import SessionHelper
from selenium.webdriver.common.by import By
from fixture.project import ProjectHelper
class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unreconized Browser %s" % browser)
        self.wd.implicitly_wait(1)
        self.session = SessionHelper(self)
        self.base_url = base_url
        self.project = ProjectHelper(self)

    def open_home_page(self):
        wd = self.wd
        if not wd.current_url.endswith("/mantisbt-1.2.20/"):
            wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

