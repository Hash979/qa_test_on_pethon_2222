from model.project import Project
import random
import string


def random_projectname(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_del_some_project(app):
    username = "administrator"
    password = "root"
    if len(app.soap.get_project_list(username, password)) == 0:
        app.project.create(Project(name=random_projectname("project_", 4)))
    old_projects = app.soap.get_project_list(username, password)
    project = random.choice(old_projects)
    app.project.del_project_by_id(project.id)
    new_projects = app.soap.get_project_list(username, password)
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)