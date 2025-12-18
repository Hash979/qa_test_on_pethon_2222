import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseurl'])
    fixture.session.ensure_login("administrator", "root")
    return fixture



@pytest.fixture(scope="session",autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
