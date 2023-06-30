import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create the web driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


def scrape_publication_names():
    # Navigate to the publications page
    driver.get('https://electrosense.org/publications')

    # Wait for the publications to load
    time.sleep(2)

    # Find all publication blocks
    publication_blocks = driver.find_elements(By.CSS_SELECTOR, 'blockquote.publication')

    # Extract the names from the publication blocks
    names = []
    for block in publication_blocks:
        text = block.text
        name_start_index = text.find('\n') + 1
        name_end_index = text.find('\n', name_start_index)
        name = text[name_start_index:name_end_index].strip()
        names.append(name)

    # Close the WebDriver
    driver.quit()

    return names


def split_names(dataset):
    new_dataset = []
    for entry in dataset:
        names = entry.split(', ')
        for name in names:
            new_dataset.append(name)
    return new_dataset


import re

import re


def check_name_matches(dataset1, dataset2):
    for entry in dataset1:
        entry['publication_ElectoSense'] = False  # Initialize the field as False

        # Extract the first name and last name from dataset1 entry
        name_parts = entry['Name'].split(' ')
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])

        for name in dataset2:
            name_parts = re.findall(r'[A-Za-z]+', name)  # Extract individual name parts

            # Check if the initials match and the last name is present in the name from dataset2
            if entry['Name'][0].lower() == name_parts[0][0].lower() and last_name.lower() in ' '.join(
                    name_parts).lower():
                entry['publication_ElectoSense'] = True  # Update the field to True
                break  # No need to continue checking once a match is found

    return dataset1


def electroSense_publications(dataset):
    # Call the function to scrape the publication names
    publication_names = scrape_publication_names()

    new_dataset = split_names(publication_names)

    updated_dataset = check_name_matches(dataset, new_dataset)

    for x in updated_dataset:
        print(x)

    print("Scraped ElectroSenses publications")
    return updated_dataset
