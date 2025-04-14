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
    time.sleep(3)

    try:
        driver.find_element(By.CLASS_NAME, "message-anywhere-button").click()
        time.sleep(2)

        # Attempt InMail message box (contenteditable div)
        try:
            message_box = driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
        except:
            message_box = driver.find_element(By.TAG_NAME, "textarea")

        subject = subject_template.render(person)
        message = message_template.render(person)
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        # Try to fill subject if input is present (for InMail)
        try:
            subject_input = driver.find_element(By.CSS_SELECTOR, 'input[name="subject"]')
            subject_input.clear()
            subject_input.send_keys(subject)
        except:
            pass  # Subject field might not exist depending on message type

        # Type the message into the message box
        message_box.click()
        message_box.send_keys(message)
        time.sleep(1)

        # Try to find and click the send button
        try:
            send_button = driver.find_element(By.XPATH, "//button[contains(., 'Send')]")
            if send_button.is_enabled():
                send_button.click()
            else:
                print("Send button is disabled.")
        except Exception as e:
            print(f"Could not find or click send button: {e}")

        return True
    except Exception as e:
        print(f"Failed to message {person['name']}: {e}")
        return False