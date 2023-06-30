from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm
import traceback
from multiprocessing import Pool, cpu_count, Manager
from time import sleep
import logging

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.ERROR)

def get_publications_count(url):
    """
    Function to scrape Google Scholar and get the total number of publications for a given scholar.

    This function uses Selenium to load the Google Scholar profile, repeatedly click the "Show more"
    button until all publications are loaded, and then count the total number of publications.

    Args:
    url (str): The URL of the Google Scholar profile.

    Returns:
    int: The total number of publications.
    """
    # Configure the Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    while True:
        try:
            # Wait until the "Show more" button is clickable, then click it
            show_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'gsc_bpf_more')))
            show_more_button.click()
        except Exception as e:
            # If the "Show more" button is not found or not clickable, we've loaded all publications
            print("Loaded all publications.")
            break

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the publication entries. Each one is a 'tr' with class 'gsc_a_tr'
    publications = soup.find_all('tr', {'class': 'gsc_a_tr'})

    # Close the browser
    driver.quit()

    # Return the count of publication entries
    return len(publications)


def infer_full_name_from_google_scholar(name):
    """
    Can take parts of names and infer the full name via Google Scholar

    :param name: the name of the individual you want to infer the full name
    :return: returns the full name normalized in unicode
    """

    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    # Get the Google Scholar profile URL
    profile_url = get_google_scholar_profile_url(name)

    # Visit the Google Scholar profile page
    driver.get(profile_url)

    # Extract the full name
    full_name = ""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gsc_prf_in")))
        full_name_elem = driver.find_element(By.CSS_SELECTOR, "#gsc_prf_in")
        full_name = full_name_elem.text
    except Exception as e:
        print("Failed to extract full name for:", name)
        print("Error:", str(e))

    driver.quit()

    # Calls a unicode normalization before returning
    return normalize_names(full_name)


def get_publications_from_scholar_profile(url):
    """
    Is a setup function that contains a loop to iterate through all iterations
    of a specific Google Scholar user.

    :param url: takes the URL to the specific Scholar Profile.
    :return: a list with all publications containing: title, all authors, and publication date.
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    # Navigate to the Google Scholar profile page
    driver.get(url)

    # Get total publications count and calculate 90% of it
    total_publications = get_publications_count(url)
    publications_to_iterate = int(total_publications * 0.9)

    print(publications_to_iterate)

    # List to store publication information
    publications = []

    # Extract publications on the current page
    publications += extract_publication_details(driver)

    # Create a progress bar with the total number of iterations
    pbar = tqdm(total=publications_to_iterate)

    try:
        # Iterate through multiple pages of publications (if available)
        for i in range(20, publications_to_iterate, 20):  # Start from 20 to skip the first iteration
            next_url = f"{url}&cstart={i}"
            driver.get(next_url)
            publications += extract_publication_details(driver)

            # Update the progress bar
            pbar.update(20)
    finally:
        pbar.n = pbar.total
        pbar.refresh()
        pbar.close()

    # Close the browser window
    driver.quit()

    return publications


def extract_publication_details(driver):
    """
    This function is called by every iteration of the loop in the
    get_publications_from_scholar_profile() function.
    It clicks on every single publication of the Scholar page and extracts:
    title, all authors, and publication date.


    :param driver: takes the driver of a Google Scholar page with a range of publications.
    :return: title, all authors, and publication date from all publications of this 20 badge.
    """

    # List to store publication information on a page
    publications = []

    # Find all publication elements on the page
    publication_elements = driver.find_elements(By.CSS_SELECTOR, '.gsc_a_tr')

    # Extract information for each publication
    for element in publication_elements:
        # Open the publication details page
        title_elem = element.find_element(By.CSS_SELECTOR, '.gsc_a_t a')
        title = title_elem.text

        # Get the publication details URL
        details_url = title_elem.get_attribute('href')

        # Open the publication details URL in a new tab
        driver.execute_script("window.open(arguments[0]);", details_url)
        driver.switch_to.window(driver.window_handles[-1])

        # Extract detailed information from the publication page
        authors = extract_authors(driver)
        date = extract_date(driver)

        # Normalize authors
        authors = normalize_names(authors)

        # Create a dictionary with publication information
        publication_info = {"Title": title, "Authors": authors, "Publication date": date}

        # Add publication info to the list
        publications.append(publication_info)

        # Close the publication details tab
        driver.close()

        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

    return publications


def extract_authors(driver):
    """
    This is called by every iteration on every paper from the extract_publication_details()
    and retrieves the name of the coauthors

    :param driver: to the specific publication page
    :return: the name of every coauthor
    """
    # Find the authors element on the publication page
    authors_elem = driver.find_element(By.CSS_SELECTOR, '.gs_scl .gsc_oci_value')
    authors = authors_elem.text

    return authors


def extract_date(driver):
    """
    This is called by every iteration on every paper from the extract_publication_details()
    and retrieves the publication date of a paper

    :param driver: to the specific publication page
    :return: the publication date of a paper
    """
    # Find the publication date element on the publication page
    try:
        date_elem = driver.find_element(By.XPATH,
                                        '//div[contains(@class, "gs_scl") and div[contains(@class, "gsc_oci_field") and text()="Publication date"]]/div[contains(@class, "gsc_oci_value")]')
        date = date_elem.text
    except NoSuchElementException:
        date = ""

    return date


def normalize_names(authors):
    """
    Normalizes names to remove all special characters and replaces them with unicode.

    :param authors: List of authors.
    :return: List of authors without special characters.
    """
    # Split authors by comma and apply normalization to each author
    normalized_authors = [unidecode(author.strip()) for author in authors.split(",")]
    return ", ".join(normalized_authors)


def count_collaborations(publications, author):
    """
    Counts the number of collaborations between the specified author and other authors in a list of publications.

    :param publications: A list of publications containing information such as authors.
    :param author: The name of the author for whom the collaborations are counted.
    :return: A sorted list of tuples representing the collaborations in descending order of the collaboration counts.
             Each tuple contains the collaborator's name and the number of collaborations.
    """
    collaboration_counts = {}

    # Iterate through each publication
    for publication in publications:
        # Get the list of authors for the current publication
        authors = publication["Authors"].split(", ")

        # Skip the specified author
        if author in authors:
            authors.remove(author)

        # Count collaborations with other authors
        for collaborator in authors:
            if collaborator in collaboration_counts:
                collaboration_counts[collaborator] += 1
            else:
                collaboration_counts[collaborator] = 1

    # Sort the collaboration counts in descending order
    sorted_collaborations = sorted(collaboration_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_collaborations


def get_collaborator_info(collaborator_info, progress):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    collaborator = collaborator_info.get("Name")
    count = collaborator_info.get("Collaborations")
    iteration = collaborator_info.get("Iteration")

    try:
        profile_url = get_google_scholar_profile_url(collaborator)
    except TimeoutException as e:
        print(f"TimeoutException occurred for {collaborator}: {str(e)}")
        driver.quit()
        progress.append(1)
        return {"Name": collaborator, "Collaborations": count, "Institution": None,
                "ImageLink": None, "Iteration": iteration}

    if "scholar.google" not in profile_url:
        print(f"Skipping {collaborator} - Not a Google Scholar link: {profile_url}")
        driver.quit()
        progress.append(1)
        return {"Name": collaborator, "Collaborations": count, "Institution": None,
                "ImageLink": None, "Iteration": iteration}

    driver.get(profile_url)
    institution = ""
    image_link = ""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gsc_prf_il")))
        institution_elem = driver.find_element(By.CSS_SELECTOR, "div.gsc_prf_il")
        institution = institution_elem.text
    except Exception as e:
        print(f"Failed to extract institution for: {collaborator}\nError: {str(e)}\nPage source: {driver.page_source}")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#gsc_prf_pua")))
        image_elem = driver.find_element(By.CSS_SELECTOR, "div#gsc_prf_pua img")
        image_link = image_elem.get_attribute("src")
    except Exception as e:
        print(f"Failed to extract image link for: {collaborator}\nError: {str(e)}\nPage source: {driver.page_source}")

    driver.quit()
    progress.append(1)

    return {"Name": collaborator, "Collaborations": count, "Institution": institution,
            "ImageLink": image_link, "Iteration": iteration}


def scrape_collaborator_info_on_google_scholar(collaborations, iteration, top_n):
    sorted_collaborators = sorted(collaborations, key=lambda x: x.get("Collaborations"), reverse=True)
    num_collaborators = min(top_n, len(sorted_collaborators))

    with Manager() as manager:
        progress = manager.list()  # shared between processes
        pool = Pool(processes=min(num_collaborators, cpu_count()))
        # prepare the arguments for get_collaborator_info
        to_scrape = [(col, progress) for col in sorted_collaborators[:num_collaborators] if
                     col.get("Iteration") == iteration]

        # Use a try/except block to handle exceptions during multiprocessing
        try:
            result_obj = pool.starmap_async(get_collaborator_info, to_scrape)  # returns a result object
        except Exception as e:
            print(f"An exception occurred during multiprocessing: {str(e)}")
            print(traceback.format_exc())
            pool.terminate()

        # progress bar
        with tqdm(total=len(to_scrape)) as pbar:
            while True:
                if len(progress) > pbar.n:
                    pbar.update(len(progress) - pbar.n)
                if not result_obj.ready():
                    sleep(0.5)  # short delay to avoid CPU overuse
                else:
                    pbar.update(len(to_scrape) - pbar.n)  # ensure progress bar fills up
                    break

        result = result_obj.get()  # get the result
        pool.close()
        pool.join()

    # Handle remaining collaborators (if any)
    remaining = [col for col in sorted_collaborators[num_collaborators:] if col.get("Iteration") == iteration]
    for collaborator_info in remaining:
        collaborator = collaborator_info.get("Name")
        count = collaborator_info.get("Collaborations")
        result.append({"Name": collaborator, "Collaborations": count, "Institution": None, "ImageLink": None,
                       "Iteration": iteration})

    print("\nScraping complete.")

    return result


def get_google_scholar_profile_url(author_name):
    """
    Retrieves the Google Scholar profile URL for the specified author name.

    :param author_name: The name of the author for whom the Google Scholar profile URL is retrieved.
    :return: The URL of the Google Scholar profile for the specified author.
    """

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # Uncomment this line to run the script without opening a visible browser window
    driver = webdriver.Chrome(options=options)

    # Navigate to Google
    driver.get('https://www.google.com')

    # Wait for the cookies dialog to appear and click "I agree"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'L2AGLb')))
    driver.find_element(By.ID, 'L2AGLb').click()

    # Wait for the advanced options to load
    time.sleep(1)

    # Find the search field and enter the search query
    search_field = driver.find_element(By.NAME, "q")
    search_field.send_keys(f"{author_name} google scholar")
    search_field.send_keys(Keys.RETURN)

    # Wait for the search results page to load
    time.sleep(1)

    # Find the first search result and extract the link
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g a')))
    first_result_link = driver.find_element(By.CSS_SELECTOR, 'div.g a').get_attribute('href')

    # Parse the URL
    parsed_url = urllib.parse.urlparse(first_result_link)

    # Modify the language parameter to ensure English
    query_params = urllib.parse.parse_qs(parsed_url.query)
    query_params['hl'] = 'en'  # Set the language to English
    modified_query_string = urllib.parse.urlencode(query_params, doseq=True)

    # Build the modified URL with the updated language parameter
    modified_url = urllib.parse.urlunparse(parsed_url._replace(query=modified_query_string))

    # Close the WebDriver
    driver.quit()

    return modified_url


def find_matching_coauthors_with_key_company(collaborators, key_company):
    """
    Checks whether a co-author's institution matches the key company and returns the matching names.

    :param collaborators: A list of collaborator dictionaries with information such as name and institution.
    :param key_company: The key company name to check against the co-authors' institutions.
    :return: A list of names that match the key company.
    """
    matching_names = []

    for collaborator in collaborators:
        institution = collaborator["Institution"]

        if institution is not None:
            # Normalize the institution and key company names for comparison
            normalized_institution = institution.lower()
            normalized_key_company = key_company.lower()

            # Check if the normalized institution contains the normalized key company
            if normalized_key_company in normalized_institution:
                matching_names.append(collaborator["Name"])

    return matching_names


def add_iteration_to_dataset(dataset, iteration):
    """
    Add the "Iteration" field with the specified value to each entry in the dataset.

    :param dataset: The dataset to update.
    :param iteration: The value to set for the "Iteration" field.
    :return: The updated dataset.
    """
    updated_dataset = []
    for entry in dataset:
        if isinstance(entry, tuple):
            name, collaborations = entry
            updated_dataset.append({'Name': name, 'Collaborations': collaborations, 'Iteration': iteration})
        else:
            updated_dataset.append(entry)

    return updated_dataset


def merge_datasets(dataset1, dataset2):
    """
    Merge two datasets into one.

    :param dataset1: The first dataset.
    :param dataset2: The second dataset.
    :return: The merged dataset.
    """
    merged_dataset = dataset1.copy()

    for entry in dataset2:
        merged_dataset.append(entry)

    return merged_dataset


def filter_duplicates(collaborators_scraped, collaborationsB):
    """
    Remove entries from collaborationsB if their names already exist in collaborators_scraped.

    :param collaborators_scraped: A list of dictionaries representing already scraped collaborators.
    :param collaborationsB: A list of dictionaries representing additional collaborators.
    :return: The reduced dataset collaborationsB.
    """
    names_scraped = set(entry['Name'] for entry in collaborators_scraped)
    reduced_dataset = []

    for entry in collaborationsB:
        name = entry['Name']
        if name not in names_scraped:
            reduced_dataset.append(entry)

    return reduced_dataset


def scrape_google_scholar(author_name, key_company):

    print("----------------------Starting Point--------------------------")
    author_name = author_name
    key_company = key_company

    full_name = infer_full_name_from_google_scholar(author_name)
    print(f"Full name inferred: {full_name}")

    url = get_google_scholar_profile_url(full_name)
    print(f"Google Scholar profile URL: {url}")

    print("----------------------Collecting Publications--------------------------")
    publications = get_publications_from_scholar_profile(url)

    print(f"Number of publications collected: {len(publications)}")

    collaborations = count_collaborations(publications, full_name)
    print(f"Collaborations counted: {len(collaborations)}")

    iteration_value = 1
    updated_dataset = add_iteration_to_dataset(collaborations, iteration_value)
    print(f"Dataset updated: {len(updated_dataset)} records")

    print("----------------------Scraping Collaborators--------------------------")
    top_n_contributors = len(updated_dataset)
    collaborators_scraped = scrape_collaborator_info_on_google_scholar(updated_dataset, iteration_value,
                                                                       top_n_contributors)
    print(f"Number of collaborators scraped: {len(collaborators_scraped)}")

    print("----------------------Finding Matches--------------------------")
    matching_names = find_matching_coauthors_with_key_company(collaborators_scraped, key_company)
    print(f"Number of key persons found: {len(matching_names)}")
    for name in matching_names:
        print(f"Key Person: {name}")

    for updated_name in matching_names:
        iteration_value += 1
        url = get_google_scholar_profile_url(updated_name)
        print(f"Google Scholar profile URL for key person: {url}")

        print("----------------------Collecting Publications for Key Person--------------------------")
        b_publications = get_publications_from_scholar_profile(url)

        b_collaborations = count_collaborations(b_publications, updated_name)
        updated_b_dataset = add_iteration_to_dataset(b_collaborations, iteration_value)

        reducedDataset = filter_duplicates(collaborators_scraped, updated_b_dataset)
        print(f"Reduced dataset size: {len(reducedDataset)}")

        print("----------------------Scraping Collaborators for Key Person--------------------------")
        collaborators_b_scraped = scrape_collaborator_info_on_google_scholar(reducedDataset, iteration_value,
                                                                             len(reducedDataset))

        merged_dataset = merge_datasets(collaborators_scraped, collaborators_b_scraped)
        collaborators_scraped = merged_dataset
        print(f"Merged dataset size: {len(merged_dataset)}")

    print("----------------------Final Scholar Dataset--------------------------")
    print("Finished Google Scholar Scrape")
    print(f"Total number of collaborators in final dataset: {len(collaborators_scraped)}")

    return collaborators_scraped
