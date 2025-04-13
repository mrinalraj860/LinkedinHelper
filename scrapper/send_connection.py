from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def connect_if_requested(driver, user, send_connect):
    if not send_connect:
        return

    print(f"Attempting to connect with: {user['name']}")

    try:
        # Find and click the "Connect" button
        connect_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Connect']]"))
        )
        connect_button.click()
        print("Clicked 'Connect'.")

        # Wait and click "Send without a note"
        send_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Send without a note']]"))
        )
        send_button.click()
        print("Connection request sent.")

        time.sleep(1)

    except TimeoutException:
        print(f"No connect button found for {user['name']}. Skipping.")
    except Exception as e:
        print(f"Error connecting with {user['name']}: {e}")