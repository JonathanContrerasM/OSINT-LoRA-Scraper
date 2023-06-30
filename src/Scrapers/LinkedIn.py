import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import requests
from dotenv import load_dotenv
import os


def get_linkedin_url(person_name):
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # Uncomment this line to run the script without opening a visible browser window
    driver = webdriver.Chrome(options=options)

    # Navigate to Google
    driver.get('https://www.google.com')

    # Wait for the cookies dialog to appear and click "I agree"
    WebDriverWait(driver, 10).until(presence_of_element_located((By.ID, 'L2AGLb')))
    driver.find_element(By.ID, 'L2AGLb').click()

    # Search for the LinkedIn profile
    search_query = f'{person_name} LinkedIn'
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_query)
    time.sleep(0.5)  # Add a 500ms (0.5s) delay to allow the search page to fully load
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to appear and get the first result's URL
    WebDriverWait(driver, 10).until(presence_of_element_located((By.CSS_SELECTOR, 'div.g a')))
    first_result_link = driver.find_element(By.CSS_SELECTOR, 'div.g a').get_attribute('href')

    # Print the first result's URL to the console
    print(f'LinkedIn profile for {person_name}: {first_result_link}')

    # Close the browser window
    driver.quit()

    print(first_result_link)

    return first_result_link


load_dotenv()  # take environment variables from .env.
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
#PROXYCURL_API_KEY = 'DEMO_MODE'



def get_profile(profile_id):
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    header_dic = {'Authorization': 'Bearer ' + PROXYCURL_API_KEY}
    params = {
        'url': f'{profile_id}',
        'fallback_to_cache': 'on-error',
        'use_cache': 'if-present',
        'skills': 'include',
        'inferred_salary': 'include',
        'personal_email': 'include',
        'personal_contact_number': 'include',
        'twitter_profile_id': 'include',
        'facebook_profile_id': 'include',
        'github_profile_id': 'include',
        'extra': 'include',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=header_dic)
    print(response.status_code)  # Add this line

    if response.status_code != 200:
        print("Likely that you have reached the end of free requests. Switching to alternative mode")
        # Return the default data if the request was not successful
        return {
            "public_identifier": "alberto-huertas-a68242182",
            "profile_pic_url": "https://media.licdn.com/dms/image/C5603AQE9-8_nj6dJPg/profile-displayphoto-shrink_400_400/0/1558020609971?e=1688601600&v=beta&t=WsGTosKCQGTLqAD5pwxz2xAAQQufB8L0OsJOR0As1Zw",
            "background_cover_image_url": None,
            "first_name": "Alberto",
            "last_name": "Huertas",
            "full_name": "Alberto Huertas",
            "follower_count": None,
            "occupation": "Postdoctoral Researcher at University of Zurich",
            "headline": "Postdoctoral Researcher at University of Zurich",
            "summary": "http://webs.um.es/alberto.huertas/",
            "country": "CH",
            "country_full_name": "Switzerland",
            "city": "Zurich",
            "state": "Zurich",
            "experiences": [{
                "starts_at": {"day": 1, "month": 10, "year": 2020},
                "ends_at": None,
                "company": "University of Zurich",
                "company_linkedin_profile_url": "https://www.linkedin.com/school/uzh/",
                "title": "Postdoctoral Researcher",
                "description": None,
                "location": "Zurich, Switzerland",
                "logo_url": "https://media.licdn.com/dms/image/C4D0BAQEi1fl1yzka5A/company-logo_400_400/0/1553675499168?e=1691020800&v=beta&t=JVZiG_3kHIFT7hGXBOynbm99n0NGH7YW_JoMAF1D1s0"
            }, {
                "starts_at": {"day": 1, "month": 6, "year": 2018},
                "ends_at": {"day": 1, "month": 10, "year": 2020},
                "company": "Waterford Institute of Technology",
                "company_linkedin_profile_url": "https://www.linkedin.com/school/waterford-institute-of-technology/",
                "title": "Postdoctoral Researcher",
                "description": "Research topics: cybersecurity in brain-computer interfaces, continuous authentication in the IoT, machine and deep learning applied to cybersecurity in networks and clinical environments",
                "location": None,
                "logo_url": "https://media.licdn.com/dms/image/C4E0BAQFcP70caTZY6w/company-logo_400_400/0/1677233297838?e=1691020800&v=beta&t=_jEIn-Up9lUBPspyAsQiXyRAdOu_EIb0W9uvV_US82U"
            }, {
                "starts_at": {"day": 1, "month": 3, "year": 2017},
                "ends_at": {"day": 1, "month": 5, "year": 2018},
                "company": "Computer Science Faculty, University of Murcia (FIUM)",
                "company_linkedin_profile_url": "https://www.linkedin.com/company/facultad-de-inform-tica-de-la-universidad-de-murcia-fium-/",
                "title": "Postdoctoral Researcher",
                "description": "Research topics: Continuous authentication in the IoT, cybersecurity in computer networks, GDPR",
                "location": "Murcia Area, Spain",
                "logo_url": "https://media.licdn.com/dms/image/C560BAQE4_0M3DtlqPw/company-logo_400_400/0/1540193993218?e=1691020800&v=beta&t=c4dVYHQCv9m_-OhVLcrlCbhh0L75ms94NXViWGzR_2w"
            }, {
                "starts_at": {"day": 1, "month": 5, "year": 2013},
                "ends_at": {"day": 1, "month": 1, "year": 2017},
                "company": "Computer Science Faculty, University of Murcia (FIUM)",
                "company_linkedin_profile_url": "https://www.linkedin.com/company/facultad-de-inform-tica-de-la-universidad-de-murcia-fium-/",
                "title": "PHD Student",
                "description": "Main topics: cybersecurity, privacy-preserving frameworks, context-awareness, location-based services, network management, network function virtualization, software-defined networks, eHealth, integrated clinical environments,",
                "location": "Murcia Area, Spain",
                "logo_url": "https://media.licdn.com/dms/image/C560BAQE4_0M3DtlqPw/company-logo_400_400/0/1540193993218?e=1691020800&v=beta&t=c4dVYHQCv9m_-OhVLcrlCbhh0L75ms94NXViWGzR_2w"
            }, {
                "starts_at": {"day": 1, "month": 11, "year": 2012},
                "ends_at": {"day": 1, "month": 4, "year": 2013},
                "company": "NEC Laboratories Europe GmbH",
                "company_linkedin_profile_url": "https://www.linkedin.com/company/nec-laboratories-europe-gmbh/",
                "title": "Computer Science Engineer",
                "description": "Main topics: cybersecurity, searchable encryption, and homomorphic algorithms",
                "location": "Heidelberg Area, Germany",
                "logo_url": "https://media.licdn.com/dms/image/C4E0BAQGDhUy-enEi7g/company-logo_400_400/0/1658309576015?e=1691020800&v=beta&t=HIe_xKvT_THqjMbNHaaWQVh2gHCh4VmqCa3f293D65Y"
            }],
            "education": [{
                "starts_at": None,
                "ends_at": {"day": 1, "month": 1, "year": 2017},
                "field_of_study": "Computer Science",
                "degree_name": "Doctor of Philosophy - PhD",
                "school": "Universidad de Murcia",
                "school_linkedin_profile_url": None,
                "description": None,
                "logo_url": "https://media.licdn.com/dms/image/C560BAQEHbI47eks5cA/company-logo_400_400/0/1591439694648?e=1691020800&v=beta&t=adnkOCxbqCNmxMF-DHTRRmdIFJm_x0fkWG3cDCZodmk",
                "grade": None,
                "activities_and_societies": None
            }, {
                "starts_at": None,
                "ends_at": {"day": 1, "month": 1, "year": 2012},
                "field_of_study": "Computer Science",
                "degree_name": "Master's degree",
                "school": "Universidad de Murcia",
                "school_linkedin_profile_url": None,
                "description": None,
                "logo_url": "https://media.licdn.com/dms/image/C560BAQEHbI47eks5cA/company-logo_400_400/0/1591439694648?e=1691020800&v=beta&t=adnkOCxbqCNmxMF-DHTRRmdIFJm_x0fkWG3cDCZodmk",
                "grade": None,
                "activities_and_societies": None
            }, {
                "starts_at": None,
                "ends_at": {"day": 1, "month": 1, "year": 2011},
                "field_of_study": "Computer Science",
                "degree_name": "Engineer's degree",
                "school": "Universidad de Murcia",
                "school_linkedin_profile_url": None,
                "description": None,
                "logo_url": "https://media.licdn.com/dms/image/C560BAQEHbI47eks5cA/company-logo_400_400/0/1591439694648?e=1691020800&v=beta&t=adnkOCxbqCNmxMF-DHTRRmdIFJm_x0fkWG3cDCZodmk",
                "grade": None,
                "activities_and_societies": None
            }],
            "languages": ["English", "Italian", "Spanish"],
            "accomplishment_organisations": [],
            "accomplishment_publications": [{
                "name": "Dynamic Network Slicing Management of Multimedia Scenarios for Future Remote Healthcare",
                "publisher": "Multimedia Tools and Applications",
                "published_on": {"day": 1, "month": 1, "year": 2019},
                "description": None,
                "url": "https://doi.org/10.1007/s11042-019-7283-3"
            }, {
                "name": "Intelligent and Dynamic Ransomware Spread Detection and Mitigation in Integrated Clinical Environments",
                "publisher": "Sensors",
                "published_on": {"day": 1, "month": 1, "year": 2019},
                "description": None,
                "url": "https://doi.org/10.3390/s19051114"
            }, {
                "name": "Mitigation of Cyber Threats: Protection Mechanisms in Federated SDN/NFV Infrastructures for 5G within FIRE+",
                "publisher": "Concurrency and Computation",
                "published_on": {"day": 1, "month": 1, "year": 2019},
                "description": None,
                "url": "https://doi.org/10.1002/cpe.5132"
            }, {
                "name": "Dynamic Management of a Deep Learning-Based Anomaly Detection System for 5G Networks",
                "publisher": "Journal of Ambient Intelligence and Humanized Computing",
                "published_on": {"day": 1, "month": 1, "year": 2018},
                "description": None,
                "url": "https://doi.org/10.1007/s12652-018-0813-4"
            }, {
                "name": "Improving the Security and QoE in Mobile Devices through an Intelligent and Adaptive Continuous Authentication System",
                "publisher": "Sensors",
                "published_on": {"day": 1, "month": 1, "year": 2018},
                "description": None,
                "url": "https://doi.org/10.3390/s18113769"
            }, {
                "name": "Sustainable securing of Medical Cyber-Physical Systems for the healthcare of the future",
                "publisher": "Sustainable Computing: Informatics and Systems",
                "published_on": {"day": 1, "month": 1, "year": 2018},
                "description": None,
                "url": "https://doi.org/10.1016/j.suscom.2018.02.010"
            }, {
                "name": "Towards the autonomous provision of self-protection capabilities in 5G networks,\"",
                "publisher": "Journal of Ambient Intelligence and Humanized Computing",
                "published_on": {"day": 1, "month": 1, "year": 2018},
                "description": None,
                "url": "https://doi.org/10.1007/s12652-018-0848-6"
            }, {
                "name": "Dynamic reconfiguration in 5G mobile networks to proactively detect and mitigate botnets",
                "publisher": "IEEE Internet Computing",
                "published_on": {"day": 1, "month": 1, "year": 2017},
                "description": None,
                "url": "https://doi.org/10.1109/MIC.2017.3481345"
            }, {
                "name": "Enabling highly dynamic mobile scenarios with Software Defined Networking",
                "publisher": "IEEE Communications Magazine",
                "published_on": {"day": 1, "month": 1, "year": 2017},
                "description": None,
                "url": "https://doi.org/10.1109/MCOM.2017.1600117CM"
            }, {
                "name": "Preserving patients' privacy in health scenarios through a multicontext-aware system,\" ",
                "publisher": "Annals of Telecommunications",
                "published_on": {"day": 1, "month": 1, "year": 2017},
                "description": None,
                "url": "http://dx.doi.org/10.1007/s12243-017-0582-7"
            }, {
                "name": "Design of a recommender system based on users' behavior and collaborative localization and tracking",
                "publisher": "Journal of Computational Science",
                "published_on": {"day": 1, "month": 1, "year": 2016},
                "description": None,
                "url": "http://doi.org/10.1016/j.jocs.2015.11.010"
            }, {
                "name": "Policy-based management for green mobile networks through Software-Defined Networking",
                "publisher": "Mobile Networks and Applications",
                "published_on": {"day": 1, "month": 1, "year": 2016},
                "description": None,
                "url": "https://doi.org/10.1007/s11036-016-0783-8"
            }, {
                "name": "Resolving privacy-preserving relationships over outsourced encrypted data storages",
                "publisher": " International Journal of Information Security",
                "published_on": {"day": 1, "month": 1, "year": 2016},
                "description": None,
                "url": "https://doi.org/10.1109/JSYST.2013.2297707"
            }, {
                "name": "PRECISE: Privacy-aware recommender based on context information for Cloud service environments",
                "publisher": "IEEE Communications Magazine",
                "published_on": {"day": 1, "month": 1, "year": 2014},
                "description": None,
                "url": "https://doi.org/10.1109/MCOM.2014.6871675"
            }, {
                "name": "SeCoMan: A semantic-aware policy framework for developing privacy-preserving and context-aware smart applications",
                "publisher": "IEEE Systems Journal",
                "published_on": {"day": 1, "month": 1, "year": 2014},
                "description": None,
                "url": "https://doi.org/10.1109/JSYST.2013.2297707"
            }],
            "accomplishment_honors_awards": [],
            "accomplishment_patents": [],
            "accomplishment_courses": [],
            "accomplishment_projects": [],
            "accomplishment_test_scores": [],
            "volunteer_work": [],
            "certifications": [],
            "connections": None,
            "people_also_viewed": [{
                "link": "https://www.linkedin.com/in/br-rodrigues",
                "name": "Bruno Rodrigues",
                "summary": "Senior Researcher at University of Zurich",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/katharina-o-e-m\u00fcller-66495213b",
                "name": "Katharina O. E.  M\u00fcller",
                "summary": "PhD Student and Junior Researcher at University of Zurich",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/chao-feng-177b171a2",
                "name": "Chao Feng",
                "summary": "Research Assistant at CSG",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/vonderassen",
                "name": "Jan von der Assen",
                "summary": "Research Assistant",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/murielfranco",
                "name": "Muriel Figueredo Franco",
                "summary": "Ph.D. | Cybersecurity | Risk Assessment | Computer Networks | Cybersecurity Economics | Project Management",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/eryk-schiller-a460744",
                "name": "Eryk Schiller",
                "summary": "Senior Researcher in Wireless Communications, Cloud Computing, Distributed Systems, and Blockchain",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/pchrysostomou",
                "name": "Panayiotis C.",
                "summary": "Technical Contractor",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/christiankiller",
                "name": "Christian Killer",
                "summary": "Web3 Security Researcher, Founder, PhD Candidate",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/robertomagancarrion",
                "name": "Roberto Mag\u00e1n Carri\u00f3n",
                "summary": "Assistant Professor at Universidad de Granada",
                "location": None
            }, {
                "link": "https://www.linkedin.com/in/javier-viadel-moreno-44752a107",
                "name": "JAVIER VIADEL MORENO",
                "summary": "CONTABLE Y FINANCIERO EN IN SIDE LOGISTICS SL",
                "location": None
            }],
            "recommendations": [],
            "activities": [],
            "similarly_named_profiles": [],
            "articles": [],
            "groups": [],
            "phone_numbers": [],
            "social_networking_services": [],
            "skills": ["Brain-computer Interfaces", "Network Function Virtualization", "eHealth", "Machine Learning",
                       "General Data Protection Regulation (GDPR)", "Deep Learning", "Network Security",
                       "Cybersecurity", "Data Privacy", "Privacy Policies", "Virtualization"],
            "inferred_salary": {"min": 45000.0, "max": 35000.0},
            "gender": "male",
            "birth_date": None,
            "industry": None,
            "extra": {"github_profile_id": None, "twitter_profile_id": None, "facebook_profile_id": None},
            "interests": [],
            "personal_emails": [],
            "personal_numbers": []
        }

    else:
        return response.json()


