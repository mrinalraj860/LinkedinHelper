from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)