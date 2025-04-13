from selenium.webdriver.common.by import By
import time
from jinja2 import Template

def load_template(subject_path, message_path):
    with open(subject_path) as f1, open(message_path) as f2:
        subject = Template(f1.read())
        message = Template(f2.read())
    return subject, message

def send_message(driver, person, subject_template, message_template):
    driver.get(person["profile_url"])
    time.sleep(2)

    try:
        driver.find_element(By.CLASS_NAME, "message-anywhere-button").click()
        time.sleep(2)
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        message = message_template.render(person)
        textarea.send_keys(message)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]").click()
        return True
    except Exception as e:
        print(f"Failed to message {person['name']}: {e}")
        return False