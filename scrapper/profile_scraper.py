from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from messenger.message_sender import load_template, send_message
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def search_and_scrape(driver, query_url, num_pages=1, args=None):
    results = []
    print(f"Navigating to search URL: {query_url}")
    driver.get(query_url)
    time.sleep(5)

    for page in range(num_pages):
        print(f"\nScraping page {page + 1}...")

        # Save current search page URL
        current_search_url = driver.current_url

        soup = BeautifulSoup(driver.page_source, "html.parser")
        user_list = []

        for li in soup.find_all("li", class_="NirxhAVFVSlawsnbhSUbXSzVfDOijnyPIDIs"):  # Adjust class if needed
            anchor = li.find("a", href=True)
            if anchor and anchor.get("href"):
                link = anchor["href"]
                if not link.startswith("http"):
                    link = "https://www.linkedin.com" + link

                name = ""
                span = li.find("span", {"aria-hidden": "true"})
                if span:
                    name = span.get_text(strip=True)

                if name:
                    print(name)
                    user_list.append({"name": name, "profile_url": link})

        for user in user_list:
            print(f"Visiting: {user['name']} → {user['profile_url']}")
            try:
                driver.get(user['profile_url'])
                time.sleep(5)

                if args and args.connect:
                    try:
                        pending_button = driver.find_element(By.XPATH, "//button[contains(., 'Pending')]")
                        print(f"Connection request already pending for {user['name']}. Skipping connection.")
                    except NoSuchElementException:
                        print(f"Attempting to connect with: {user['name']}")
                        try:
                            connect_button = driver.find_element(By.XPATH, "//button[contains(., 'Connect')]")
                            try:
                                connect_button.click()
                            except:
                                driver.execute_script("arguments[0].click();", connect_button)
                            time.sleep(2)
                            send_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send without a note')]"))
                            )
                            send_button.click()
                            print(f"Connection request sent to {user['name']}")
                            time.sleep(2)
                        except NoSuchElementException:
                            print(f"No connect button found for {user['name']}. Skipping.")
                        except Exception as e:
                            print(f"Error trying to connect with {user['name']}: {e}")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                except Exception as e:
                    print(f"Error while trying to load profile for {user['name']}: {e}")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "top-card-text-details-contact-info"))
                    ).click()
                    print("Contact Info button clicked.")
                    time.sleep(3)
                except NoSuchElementException:
                    print("Contact Info button not found.")
                    results.append(user)
                    continue

                soup = BeautifulSoup(driver.page_source, "html.parser")
                contact_div = soup.find("div", class_="artdeco-modal__content")
                if args and args.send:
                    print(f"Sending message to: {user['name']}")
                    full_name = user.get('name', '')
                    first_name = full_name.split()[0] if full_name else ''
                    user['first_name'] = first_name
                    
                    try:
                        subject_template, message_template = load_template("templates/subject.txt", "templates/message.txt")
                        success = send_message(driver, user, subject_template, message_template)
                        if success:
                            print(f"Message sent to {user['name']}")
                    except Exception as e:
                        print(f"Failed to send message to {user['name']}: {e}")

                        
                contact_info = {
                    "email": "", "phone": "", "birthday": "",
                    "linkedin_profile": "", "website": ""
                }
                if contact_div:
                    for section in contact_div.find_all("section", class_="pv-contact-info__contact-type"):
                        heading = section.find("h3")
                        if heading:
                            title = heading.get_text(strip=True)
                            if "Email" in title:
                                tag = section.find("a", href=lambda x: x and x.startswith("mailto:"))
                                if tag:
                                    contact_info["email"] = tag.text.strip()
                            elif "Phone" in title:
                                tag = section.find("span")
                                if tag:
                                    contact_info["phone"] = tag.text.strip()
                            elif "Birthday" in title:
                                tag = section.find("span")
                                if tag:
                                    contact_info["birthday"] = tag.text.strip()
                            elif "Website" in title:
                                tag = section.find("a")
                                if tag:
                                    contact_info["website"] = tag.text.strip()
                            elif "Profile" in title:
                                tag = section.find("a")
                                if tag:
                                    contact_info["linkedin_profile"] = tag.text.strip()

                user.update(contact_info)

            except Exception as e:
                print(f"Error scraping profile: {e}")
                user.update({
                    "email": "", "phone": "", "birthday": "",
                    "linkedin_profile": "", "website": ""
                })

            results.append(user)
            # if there is need to send message




        # Go back to search page before clicking "Next"
        print("Returning to search results page to paginate...")
        driver.get(current_search_url)
        time.sleep(3)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            next_button.click()
            print("Next button clicked.")
            time.sleep(5)
        except Exception as e:
            print("Next button not found or not clickable:", e)
            break

    return results

def save_to_excel(data, filename="data/people.csv"):
    if not filename.endswith(".csv"):
        filename += ".csv"
    if not filename.startswith("data/"):
        filename = os.path.join("data", filename)
    print(filename)
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    pd.DataFrame(data).to_csv(filename, index=False)
    print(f"\nData saved to: {filename}")
    print(f"Total profiles scraped: {len(data)}")

