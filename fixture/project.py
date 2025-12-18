from selenium.webdriver.common.by import By
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            wd.get(self.app.base_url + "manage_proj_page.php")

    def create(self, group):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element(By.CSS_SELECTOR, 'input[value="Create New Project"]').click()
        self.enter_text(group)
        wd.find_element(By.CSS_SELECTOR, 'input[value="Add Project"]').click()
        # self.return_to_groups_page()

    def enter_text(self, project):
        wd = self.app.wd
        name_field = wd.find_element(By.NAME, "name")
        name_field.click()
        name_field.clear()
        name_field.send_keys(project.name)

    def get_project_list(self):
        wd = self.app.wd
        self.open_project_page()
        self.project_cache = []

        elements = wd.find_elements(
            By.XPATH,
            "//td/a[contains(@href,'manage_proj_edit_page.php?project_id=')]"
        )

        for element in elements:
            text = element.text
            project_id = element.get_attribute("href").replace(
                self.app.base_url + "manage_proj_edit_page.php?project_id=",
                "")
            self.project_cache.append(Project(name=text, id=project_id))

        return list(self.project_cache)

    def del_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        self.enter_to_project_page_by_id(id)
        wd.find_element(By.CSS_SELECTOR, 'input[value="Delete Project"]').click()
        wd.find_element(By.CSS_SELECTOR, 'input[value="Delete Project"]').click()
        self.project_cache = None

    def enter_to_project_page_by_id(self, id):
        wd = self.app.wd
        wd.get(self.app.base_url + "manage_proj_edit_page.php?project_id=" + str(id))
