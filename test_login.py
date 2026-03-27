
!apt-get update


!apt-get install -y wget gnupg


!wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
!echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

!apt-get update
!apt-get install -y google-chrome-stable

!pip install selenium webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)
BASE_URL = "https://opensource-demo.orangehrmlive.com/"

def login(username, password):
    driver.delete_all_cookies()
    driver.get(BASE_URL)
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()

def get_error_text():
    return wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@class, 'oxd-alert')]//p"))).text

try:
    # Тест 1: Успішний логін
    print("Запуск Тест 1: Успішний логін")
    login("Admin", "admin123")
    assert "dashboard" in driver.current_url.lower()
    print("Результат Тест 1: Успішно")

    # Тест 2: Неправильний пароль
    print("Запуск Тест 2: Неправильний пароль")
    login("Admin", "wrong123")
    print(f"Результат Тест 2: Успішно (Помилка: {get_error_text()})")

    # Тест 3: Навігація в PIM
    print("Запуск Тест 3: Навігація в PIM")
    login("Admin", "admin123")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='PIM']"))).is_displayed()
    print("Результат Тест 3: Успішно")

except Exception as e:
    print(f"Помилка: {e}")
    driver.save_screenshot("error.png")

finally:
    driver.quit()
    print("Тестування завершено")

