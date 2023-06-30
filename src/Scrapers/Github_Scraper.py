import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def search_and_open_github(project):
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
    search_field.send_keys(project + " GitHub")
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

    # Wait for the GitHub page to load
    WebDriverWait(driver, 10).until(EC.url_contains("github.com"))

    # Print the current URL (GitHub page)
    print("Current URL:", driver.current_url)

    # Click on the "People" tab
    people_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="/orgs/electrosense/people"]')
    people_tab.click()

    # Wait for the website to load
    time.sleep(2)

    # Print the current URL (People section)
    print("Current URL (People section):", driver.current_url)

    # Extract the names of the people listed
    people_names = driver.find_elements(By.CSS_SELECTOR, 'ul.border-top li div.py-3.css-truncate.pl-3.flex-auto a.f4')
    names = [name.text.strip() for name in people_names]

    # Print the names
    print("People Names:")
    for name in names:
        print(name)

    print(names)

    # Close the WebDriver
    driver.quit()

    return names


def check_name_match(dataset1, dataset2):
    for entry in dataset1:
        name = entry['Name']
        if name in dataset2:
            entry['GitHub_Match'] = True
        else:
            entry['GitHub_Match'] = False
    return dataset1


def check_github(dataset, project):
    # Example usage
    github_matches = search_and_open_github(project)

    result = check_name_match(dataset, github_matches)

    print("Scraped GitHub")
    return result
