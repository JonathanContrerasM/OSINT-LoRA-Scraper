from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import os
from dotenv import load_dotenv

def scrape_ElectroSense():
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # Uncomment this line to run the script without opening a visible browser window
    driver = webdriver.Chrome(options=options)

    # Navigate to Google
    driver.get('https://www.google.com')

    # Wait for the cookies dialog to appear and click "I agree"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'L2AGLb')))
    driver.find_element(By.ID, 'L2AGLb').click()

    # Wait for the advanced options to load
    time.sleep(2)

    # Find the search field and enter the search query
    search_field = driver.find_element(By.NAME, "q")
    search_field.send_keys(f"ElectroSense")
    search_field.send_keys(Keys.RETURN)

    # Wait for the search results page to load
    time.sleep(2)

    # Find the first search result and extract the link
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g a')
    first_result = search_results[0]
    link = first_result.get_attribute('href')

    # Click on the first search result
    first_result.click()

    # Wait for the website to load
    time.sleep(2)

    # Navigate to the "Partners" sub-register site
    driver.get(link + '/partners')

    # Wait for the "Partners" page to load
    time.sleep(2)

    # Find the content section of the page
    content_section = driver.find_element(By.XPATH, '/html/body/div[3]/partners-page/div/div/div')

    # Find all the links within the content section
    content_links = content_section.find_elements(By.TAG_NAME, 'a')

    # Extract the links, excluding the navbar and footer links
    valid_links = []
    for link in content_links:
        href = link.get_attribute('href')
        if href and not href.startswith('#navbar') and not href.startswith('#footer'):
            valid_links.append(href)

    # Close the browser
    driver.quit()

    return valid_links


def chat_with_gpt3(question):
    load_dotenv()
    api_key = os.getenv("OPEN_AI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    # Extract the assistant's reply
    assistant_reply = response_json['choices'][0]['message']['content']

    return response_json


def check_institution_match(response_institutions, dataset):
    """
    Checks if the institution of each person in the dataset matches any of the provided names from the response.
    Adds a field indicating the match status and the matched institution.

    :param response_institutions: A string containing the company and university names from the response.
    :param dataset: A list of dictionaries representing the dataset.
    :return: The updated dataset with additional fields indicating the institution match status and the matched institution.
    """
    # Split the response institutions string into a list of individual institution names
    response_institutions = [name.strip() for name in response_institutions.split(',')]

    # Iterate through each person in the dataset
    for person in dataset:
        institution = person['Institution']
        matched_institution = None

        if institution is not None:
            # Check if the person's institution matches any of the response institutions
            for response_institution in response_institutions:
                if response_institution.lower() in institution.lower():
                    matched_institution = response_institution
                    break

        # Add fields indicating the match status and the matched institution
        person['InstitutionMatch'] = matched_institution
        person['InstitutionMatchStatus'] = matched_institution is not None

    return dataset


def electroSense(dataset):
    links = scrape_ElectroSense()
    print(links)

    question = "I will give you a list of URLs. Can you infer the name of the company or university with these URLs?\n\n"
    question += "URLs:\n"
    for link in links:
        question += f"- {link}\n"
    question += "\nPlease only return the names in a CSV format and no explanations."

    response = chat_with_gpt3(question)

    print(response['choices'][0]['message']['content'])

    updated_dataset = check_institution_match(response['choices'][0]['message']['content'], dataset)

    print("Scraped electroSense")
    return updated_dataset
