from selenium.webdriver.common.by import By
import time
from jinja2 import Template
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def load_template(subject_path, message_path):
    with open(subject_path) as f1, open(message_path) as f2:
        subject = Template(f1.read())
        message = Template(f2.read())
    return subject, message

def send_message(driver, person, subject_template, message_template):
    driver.get(person["profile_url"])
    time.sleep(3)

    try:
        # Click only the primary (blue) 'Message' button
        try:
            message_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'artdeco-button--primary') and .//span[text()='Message']]"
                ))
            )
            driver.execute_script("arguments[0].click();", message_button)
            print(" Message button clicked.")
            time.sleep(5)
        except Exception as e:
            print(f" Could not find or click Message button: {e}")
            return False

        # Try finding the message box
        try:
            message_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
            )
        except:
            try:
                message_box = driver.find_element(By.TAG_NAME, "textarea")
            except Exception as e:
                print(f" Could not find message input: {e}")
                return False

        # Prepare subject and message content
        subject = subject_template.render(person)
        message = message_template.render(person)
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        # Fill in subject if present (for InMail)
        try:
            subject_input = driver.find_element(By.CSS_SELECTOR, 'input[name="subject"]')
            subject_input.clear()
            subject_input.send_keys(subject)
        except:
            pass  # Subject field might not exist

        # Fill the message
        message_box.click()
        message_box.send_keys(message)
        time.sleep(1)

        # Click the send button
        try:
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.msg-form__send-btn[type='submit']"))
            )
            if send_button.is_enabled():
                send_button.click()
                print(" Message sent.")
            else:
                print(" Send button is disabled.")
        except Exception as e:
            print(f" Could not find or click send button: {e}")
            return False

        return True

    except Exception as e:
        print(f" Failed to message {person['name']}: {e}")
        return False