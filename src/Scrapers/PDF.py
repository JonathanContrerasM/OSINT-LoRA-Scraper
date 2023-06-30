import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import codecs
import re
from unidecode import unidecode


def pdf_to_html(pdf_file, html_file):
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()

    with open(html_file, 'wb') as output_file:
        device = HTMLConverter(rsrcmgr, output_file, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        with open(pdf_file, 'rb') as input_file:
            for page in PDFPage.get_pages(input_file):
                interpreter.process_page(page)

        device.close()


filename = os.path.join(os.getcwd(), 'document.pdf')


def search_and_download_pdf(search_string1, search_string2):
    # Setup selenium webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to Google
    driver.get('https://www.google.com')

    # Wait for the cookies dialog to appear and click "I agree"
    WebDriverWait(driver, 10).until(presence_of_element_located((By.ID, 'L2AGLb')))
    driver.find_element(By.ID, 'L2AGLb').click()

    # Perform the search
    search_box = driver.find_element("name", "q")
    search_box.send_keys(f'{search_string1} {search_string2}')
    search_box.submit()

    # Wait for the results to load
    time.sleep(2)

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the first PDF link
    pdf_url = None
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'pdf' in href:
            pdf_url = href
            break

    # Download the PDF
    response = requests.get(pdf_url)
    filename = os.path.join(os.getcwd(), 'document.pdf')
    with open(filename, 'wb') as f:
        f.write(response.content)

    # Wait for the download to finish
    time.sleep(2)

    # Close the browser
    driver.quit()

    # Convert the PDF to HTML
    html_filename = os.path.join(os.getcwd(), '../out.html')
    pdf_to_html(filename, html_filename)

    # Now 'out.html' contains the PDF converted to HTML
    with open(html_filename) as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        divs = soup.find_all('div')

        # Initialize an empty string to store the matching texts
        matching_text = ""

        for div in divs:
            text = div.get_text(separator="\n")

            # Only consider divs that contain both 'LoRa' and 'OSINT'
            if 'LoRa' in text and 'OSINT' in text:
                # Append the matching text to the string with a space in between
                matching_text += text + " "

        # Remove trailing spaces and print the final text
        matching_text = matching_text.strip()

        return matching_text


def count_mentions_in_html(html_file, collaborators):
    """
    Searches the HTML file for mentions of each collaborator in the provided list and counts the number of mentions.
    Saves the normalized HTML content to a file for inspection.

    :param html_file: The path to the HTML file.
    :param collaborators: A list of dictionaries representing collaborator information.
    :return: A new list of dictionaries with the collaborator information including mention count.
    """
    # Read the HTML file using Unicode parsing
    with codecs.open(html_file, 'r', 'utf-8') as file:
        html_content = file.read()

    # Normalize the HTML content by converting special characters to ASCII equivalents
    normalized_html = unidecode(html_content)

    # Replace multiple spaces with a single space
    normalized_html = re.sub(r'\s+', ' ', normalized_html)

    # Save the normalized HTML content to a file
    with open('normalized_html.html', 'w', encoding='utf-8') as output_file:
        output_file.write(normalized_html)

    # Parse the normalized HTML content
    soup = BeautifulSoup(normalized_html, 'html.parser')

    # Create a new list to store the updated collaborator information
    updated_collaborators = []

    # Iterate through the collaborators
    for collaborator_info in collaborators:
        collaborator = collaborator_info['Name']
        count = collaborator_info['Collaborations']

        # Normalize the collaborator name by converting special characters to ASCII equivalents
        normalized_collaborator = unidecode(collaborator)

        # Find all occurrences of the normalized collaborator name in the HTML content using the soup object
        mention_count = len(soup.find_all(string=lambda text: normalized_collaborator.lower() in text.lower()))

        # Add the mention count to the collaborator's information dictionary
        collaborator_info['MentionCount'] = mention_count

        # Add the updated collaborator to the list
        updated_collaborators.append(collaborator_info)

    return updated_collaborators


def search_report(keyword, key_company):
    # Call the function
    xx = search_and_download_pdf(keyword, key_company)

    print("Finished searching for company reports")
    return xx


def check_report_collaborations(dataset):
    # Specify the path to the HTML file
    html_file_path = '../out.html'

    # Call the function to count the mentions in the HTML file
    updated_collaborators = count_mentions_in_html(html_file_path, dataset)

    print("Finished checking for collaborations with the company")
    return updated_collaborators
