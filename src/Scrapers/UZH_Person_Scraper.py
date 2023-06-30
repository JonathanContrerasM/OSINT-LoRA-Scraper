from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait


def scrape_google_search(name, company):
    # Set up Chrome WebDriver
    options = Options()
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
    search_query = name + " " + company
    search_field.send_keys(search_query)
    search_field.submit()

    # Wait for the search results page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g a')))

    # Find the first search result that is not associated with LinkedIn, Google Scholar, IEEE, or ResearchGate
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g a')
    target_link = None
    for link in search_results:
        href = link.get_attribute('href')
        if "linkedin" not in href and "scholar.google" not in href and "ieee" not in href and "researchgate" not in href:
            target_link = link
            break

    # Click on the target link
    target_link.click()

    # Wait for the page to load
    time.sleep(2)

    # Extract information from the target link
    info = scrape_personal_website(driver.current_url)

    # Close the browser window
    driver.quit()

    return info


def scrape_personal_website(url):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # Uncomment this line to run the script without opening a visible browser window
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(2)

    name = ""
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, ".Intro--title")
        name = name_element.text.strip()
    except:
        print("Failed to extract name")

    email = ""
    phone = ""
    fax = ""
    try:
        contact_element = driver.find_element(By.CSS_SELECTOR, "ul.type1")
        contact_items = contact_element.find_elements(By.TAG_NAME, "li")
        for item in contact_items:
            if "Email" in item.text:
                email = item.text.split(":")[1].strip()
            elif "Phone" in item.text:
                phone = item.text.split(":")[1].strip()
            elif "Fax" in item.text:
                fax = item.text.split(":")[1].strip()
    except:
        print("Failed to extract contact information")

    short_bio = ""
    try:
        bio_element = driver.find_element(By.XPATH, "//h2[@id='Short_Bio:']/following-sibling::div/div/p")
        short_bio = bio_element.text.strip()
    except:
        print("Failed to extract short bio")

    research_interests = []
    try:
        interests_element = driver.find_element(By.XPATH,
                                                "//h2[@id='Research_Interests:']/following-sibling::div/div/ul")
        interests_items = interests_element.find_elements(By.TAG_NAME, "li")
        for item in interests_items:
            research_interests.append(item.text.strip())
    except:
        print("Failed to extract research interests")

    projects = []
    try:
        projects_element = driver.find_element(By.XPATH, "//h2[@id='Projects:']/following-sibling::div/div/ul")
        project_elements = projects_element.find_elements(By.TAG_NAME, "li")
        for project_element in project_elements:
            project_name_element = project_element.find_element(By.TAG_NAME, "a")
            project_link = project_name_element.get_attribute("href")
            project_driver = webdriver.Chrome(options=options)
            project_driver.get(project_link)
            time.sleep(2)
            project_info = scrape_project_page(project_driver)
            projects.append(project_info)
            project_driver.quit()
    except:
        print("Failed to extract projects")

    driver.quit()

    info = {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Fax": fax,
        "Short Bio": short_bio,
        "Research Interests": research_interests,
        "Projects": projects
    }

    return info


def scrape_project_page(driver):
    project_name = ""
    general_info = {}
    project_partners = []
    uzh_personnel = []

    # Extract the project name
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "section.Intro div.Intro--top h1.Intro--title")
        project_name = name_element.text.strip()
    except:
        print("Failed to extract project name")

    # Extract the general information
    try:
        info_elements = driver.find_elements(By.XPATH,
                                             "//h2[@id='General_Information']/following-sibling::div/div/table/tbody/tr")
        for info_element in info_elements:
            key_element = info_element.find_element(By.TAG_NAME, "td")
            value_element = info_element.find_element(By.TAG_NAME, "p")
            key = key_element.text.strip().rstrip(":")
            value = value_element.text.strip()
            general_info[key] = value
    except:
        print("Failed to extract general information")

    # Extract the project partners
    try:
        partner_elements = driver.find_elements(By.XPATH, "/html/body/main/section[2]/div[5]/div/div/ul/li/a")
        project_partners = [partner_element.text.strip() for partner_element in partner_elements]
    except:
        print("Failed to extract project partners")

    # Extract the UZH personnel
    try:
        personnel_elements = driver.find_elements(By.XPATH, "/html/body/main/section[2]/div[6]/div/div/ul/li")
        for personnel_element in personnel_elements:
            personnel_name = personnel_element.text.strip()
            uzh_personnel.append(personnel_name)
    except:
        print("Failed to extract UZH personnel")

    # Return the extracted project information as a dictionary
    project_info = {
        "Project Name": project_name,
        "General Information": general_info,
        "Project Partners": project_partners,
        "UZH Personnel": uzh_personnel
    }
    return project_info

