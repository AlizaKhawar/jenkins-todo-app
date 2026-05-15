from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, pytest

BASE_URL = "http://host.docker.internal:5000"

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()

def test_page_title(driver):
    driver.get(BASE_URL)
    assert "Todo" in driver.title

def test_add_task_visible(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    inp = wait.until(EC.presence_of_element_located((By.NAME, "task")))
    inp.clear()
    inp.send_keys("Selenium test task")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    driver.get(BASE_URL)
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Selenium test task" in body
