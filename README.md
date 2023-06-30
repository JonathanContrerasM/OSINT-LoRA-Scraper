# Scraper

Welcome to the Scraper project. This tool is a web scraper powered by Python and Flask. This project was entirely designed and run on a Linux operating system.

## Prerequisites

Before you can use Scraper, make sure that you have the following software installed on your system:

- **Python**: The Scrapers are Python-based. If you don't have Python installed, you can download it from the [official Python website](https://www.python.org/downloads/). I am running Python 3.10.6

- **Chromium**: Scraper uses the Selenium WebDriver with Chromium. The project has been tested with Chromium version 114.0.5735.106. You can download Chromium from the [official Chromium website](https://www.chromium.org/getting-involved/download-chromium).

- **ChromeDriver**: This is the WebDriver for Chromium, which is necessary for Scraper to interact with the Chromium browser. Scraper has been tested with ChromeDriver version 113.0.5672.63. You can download ChromeDriver from the [ChromeDriver downloads page](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Setting up the Environment

1. **Add ChromeDriver to your PATH**: After downloading ChromeDriver, you need to add it to your system's PATH. Here's how you do it:

    - Extract the downloaded ChromeDriver archive to obtain the `chromedriver` executable.
    
    - Move the `chromedriver` executable to a directory of your choice. For example, you could put it in the `/usr/local/bin` directory, which is included in the system's PATH by default on most Linux systems. You can do this with the following command, replacing `/path/to/chromedriver` with the path where you extracted the `chromedriver` executable:

        ```bash
        sudo mv /path/to/chromedriver /usr/local/bin
        ```

    - Check that the `chromedriver` is now in your PATH by opening a new terminal window and running:

        ```bash
        chromedriver --version
        ```

      If the `chromedriver` is correctly added to your PATH, you should see its version number.

2. **Install Python Dependencies**: Scraper also depends on several Python packages, which you can install using Pip. To install these dependencies, navigate to the `Scraper/src` directory in your terminal and run the following command:

    ```bash
    pip install -r requirements.txt
    ```
   
## Setting Up API Keys

This project uses the [Proxycurl API](https://nubela.co/proxycurl) and the [OpenAI API](https://openai.com/blog/openai-api). You'll need to sign up for accounts on these platforms to get your API keys.

Follow the steps below to set up your API keys:

1. Sign up for a Proxycurl account at [https://nubela.co/proxycurl](https://nubela.co/proxycurl). After signing up, you'll be able to find your Proxycurl API key in the dashboard.

2. Sign up for an OpenAI account at [https://openai.com/blog/openai-api](https://openai.com/blog/openai-api). After signing up, navigate to the API section to find your OpenAI API key.

3. Once you have your API keys, you need to add them to a `.env` file in the root directory of the project. This file is used to securely store sensitive data such as API keys. If the file doesn't exist, create it.

4. Open the `.env` file in a text editor and add the following lines:

    ```
    PROXYCURL_API_KEY='<your-proxycurl-api-key>'
    OPEN_AI_API_KEY='<your-openai-api-key>'
    ```

Replace `<your-proxycurl-api-key>` and `<your-openai-api-key>` with your actual API keys.

5. Save and close the `.env` file. The keys are now available to your application.

Remember to never share your API keys or commit them to your source code repository. The `.env` file is usually added to the `.gitignore` file to prevent it from being tracked by Git.


## Running the Project

Once you have set up your environment and installed the necessary dependencies, you can start the Flask server by running the `main.py` script located in the `Scraper/src` directory.

Here is the command to run the script:

```bash
python3 src/main.py
```