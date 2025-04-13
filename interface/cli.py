from scrapper import login, profile_scraper
from messenger import message_sender
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

def run_cli(args):
    driver = webdriver.Chrome()

    login.login(driver, args.email, args.password)
    print(  "Logged in successfully!")
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-card"))
    )
    keywords = pd.read_csv("templates/search_list.csv")['keyword'].tolist()
    print(keywords)
    for term in keywords:
        query_url = f"https://www.linkedin.com/search/results/people/?keywords={term.replace(' ', '%20')}"
        print("query_url: ", query_url)
        people = profile_scraper.search_and_scrape(driver, query_url)
        profile_scraper.save_to_excel(people, filename=f"{term.replace(' ', '_')}.csv")

        if args.send:
            subject, message = message_sender.load_template("templates/subject.txt", "templates/message.txt")
            for person in people:
                message_sender.send_message(driver, person, subject, message)

    driver.quit()