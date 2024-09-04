# READER and DOWNLOADER

"""
    Script for reading URLs in the excel files (old&new) .
    And will download its corresponding page source in an html file output.
    The output html file will be saved in a subfolder.
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

relative_chromedriver_path = './drivers/chromedriver.exe'
relative_old_output_folder_dir = './data/old_pagesource_html_files'
relative_new_output_folder_dir = './data/new_pagesource_html_files'
relative_old_xls_filepath = './data/OLD_NOK_NHL_PAGE_LIST.xlsx'
relative_new_xls_filepath = './data/NEW_NOK_NHL_PAGE_LIST.xlsx'

dir = os.path.dirname(__file__)

chromedriver_path = os.path.join(dir, relative_chromedriver_path)
old_output_folder_dir = os.path.join(dir, relative_old_output_folder_dir)
new_output_folder_dir = os.path.join(dir, relative_new_output_folder_dir)
old_xls_filepath = os.path.join(dir, relative_old_xls_filepath)
new_xls_filepath = os.path.join(dir, relative_new_xls_filepath)

# Boolean variable to control headless mode
headless_mode = True

def initialize_webdriver(driver_path, headless=False):
    try:
        print("Initializing WebDriver...")
        options = Options()

        if headless:
            options.add_argument('--headless')

        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        if headless:
            print("-- WebDriver initialized in headless mode. --")
        else:
            print("-- WebDriver initialized successfully. --")
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        raise

def load_excel_file(file_path, sheet_names=None):
    # Read the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Use all sheet names if not provided
    if sheet_names is None:
        sheet_names = excel_file.sheet_names
    
    # Dictionary to store URLs
    url_lists = {'hk': {}, 'kr': {}}

    for sheet_name in sheet_names:
        if sheet_name not in excel_file.sheet_names:
            print(f"Warning: Sheet '{sheet_name}' does not exist in the Excel file.")
            continue
        
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        if len(df.columns) <= 1:
            print(f"Sheet '{sheet_name}' does not have a second column.")
            continue
        
        # Extract URLs for each category
        url_lists['hk'][sheet_name] = df[df.iloc[:, 1].astype(str).str.contains("https://www.nintendo.com.hk", na=False)].iloc[:, 1].tolist()
        url_lists['kr'][sheet_name] = df[df.iloc[:, 1].astype(str).str.contains("https://www.nintendo.co.kr", na=False)].iloc[:, 1].tolist()

    return url_lists

def get_page_source(url, driver, output_dir, prefix):
    try:
        print(f"...Getting page source for: {url}")
        driver.get(url)
        time.sleep(3)
    
        page_source = driver.page_source
        filename = url.replace("https://", "").replace("/", "_").replace(":", "")[:100] + ".html"
        file_path = os.path.join(output_dir, f"{prefix}_{filename}")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f"...Saved")

    except Exception as e:
        print(f"Error processing URL '{url}': {e}")

def process_urls(url_lists, driver, output_dir, prefix):
    for sheet, urls in url_lists.items():
        for url in urls:
            # print(f"Processing URL from sheet '{sheet}': {url}")
            print(f"...Processing URL from sheet '{sheet}'")
            get_page_source(url, driver, output_dir, prefix)

def create_output_directory(output_dir):
    try:
        if not os.path.exists(output_dir):
            print(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir)
    except Exception as e:
        print(f"Error creating output directory '{output_dir}': {e}")
        raise

def main():

    driver_path = chromedriver_path
    old_file_path = old_xls_filepath
    old_output_dir = old_output_folder_dir
    new_file_path = new_xls_filepath
    new_output_dir = new_output_folder_dir

    # List of sheets to be processed
    selected_sheets = ['Static']

    try:
        # Create output directories
        create_output_directory(old_output_dir)
        create_output_directory(new_output_dir)

        # Load URLs from Excel files
        old_url_lists = load_excel_file(old_file_path, selected_sheets)
        new_url_lists = load_excel_file(new_file_path, selected_sheets)

        # Initialize WebDriver
        driver = initialize_webdriver(driver_path, headless=headless_mode)

        try:
            process_urls(old_url_lists['hk'], driver, old_output_dir, 'hk')
            process_urls(new_url_lists['hk'], driver, new_output_dir, 'hk')
            process_urls(old_url_lists['kr'], driver, old_output_dir, 'kr')
            process_urls(new_url_lists['kr'], driver, new_output_dir, 'kr')
        finally:
            print("...Closing WebDriver")
            driver.quit()
    
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()