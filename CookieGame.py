from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Setting up the selenium webdriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Opening the cookie_clicker game
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Handling the cookies popup
cookies_popup = driver.find_element(By.CLASS_NAME, "fc-button-label")
cookies_popup.click()

# Selecting the language in the game
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)
lang = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
lang.click()

# Locating the big cookie element
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)
cookie = driver.find_element(By.ID, "bigCookie")

# Clicking the big cookie and purchasing upgrades
while True:
    try:
        cookie.click()
    except StaleElementReferenceException:
        cookie = driver.find_element(By.ID, "bigCookie")
        cookie.click()

    # Getting the current cookie count
    cookie_count = driver.find_element(By.ID, "cookies").text.split(" ")[0]
    cookie_count = int(cookie_count.replace(",", ""))

    # There are 4 upgrades in the game, checking if we can afford them
    for i in range(4):
        price_of_upgrade = driver.find_element(By.ID, "productPrice" + str(i)).text.replace(",", "")
        if not price_of_upgrade.isdigit():
            continue

        price_of_upgrade = int(price_of_upgrade)

        if cookie_count >= price_of_upgrade:
            upgrade = driver.find_element(By.ID, "product" + str(i))
            upgrade.click()
            break # Exit the loop after an upgrade
