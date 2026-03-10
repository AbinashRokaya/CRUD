import pytest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="session", autouse=True)
def django_server():
    """Start Django dev server before tests, stop it after."""
    server = subprocess.Popen(
        ["python", "manage.py", "runserver", "--noreload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(10)  # Wait for server to boot
    yield
    server.terminate()

@pytest.fixture
def driver():
    """Provide a fresh Chrome driver per test, quit after."""
    chrome = webdriver.Chrome()
    yield chrome
    chrome.quit()  # Always runs, even if test fails

def test_notes_can_be_created(driver):
    driver.get('http://127.0.0.1:8000/notes/add/')
    driver.find_element(By.NAME, 'title').send_keys('Django Course')
    driver.find_element(By.NAME, 'description').send_keys(
        'Complete course with urls, templates, models, etc')
    driver.find_element(By.NAME, 'submit').click()
    time.sleep(10)

    title = driver.find_element(By.TAG_NAME, 'td').text
    assert 'Django Course' in title

def test_error_occurs_if_description_is_less_than_10_chars_long(driver):
    driver.get('http://127.0.0.1:8000/notes/add/')
    driver.find_element(By.NAME, 'title').send_keys('Django Course')
    driver.find_element(By.NAME, 'description').send_keys('dj')
    driver.find_element(By.NAME, 'submit').click()
    time.sleep(2)

    error = driver.find_element(By.TAG_NAME, 'li').text
    assert 'Description must be at least 10 characters long' in error