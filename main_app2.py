# MATCHCHECK/FILECOMPARE

"""
    Script for checking/comparing of the downloaded html file (pagsource/source_code).
    It will produce html output report and an excel file.
    The output files will be stored in a subfolder named 'Result'.
"""

import os
import difflib
from beautifulsoup import compare_html_files_in_folders_bs4

relative_old_folder_path = './data/old_pagesource_html_files'
relative_new_folder_path = './data/new_pagesource_html_files'
relative_output_folder_path = './result'
dir = os.path.dirname(__file__)

old_folder_path = os.path.join(dir, relative_old_folder_path)
new_folder_path = os.path.join(dir, relative_new_folder_path)
output_folder_path = os.path.join(dir,relative_output_folder_path)

def compare_files_in_folders(old_version_folder, new_version_folder, output_folder):

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get list of files in both folders
    old_files = set(os.listdir(old_version_folder))
    new_files = set(os.listdir(new_version_folder))

    # Find common files between both folders
    common_files = old_files.intersection(new_files)

    # Initialize difflib.HtmlDiff object
    html_diff = difflib.HtmlDiff()

    # Compare each common file
    for filename in common_files:
        # Define the full file paths
        old_file_path = os.path.join(old_version_folder, filename)
        new_file_path = os.path.join(new_version_folder, filename)
        
        # Read the contents of the old and new files
        with open(old_file_path, 'r', encoding="utf-8") as old_file, open(new_file_path, 'r', encoding="utf-8") as new_file:
            old_content = old_file.readlines()
            new_content = new_file.readlines()
        
        # Create the diff HTML
        diff_html = html_diff.make_file(old_content, new_content, fromdesc=f"Old Version: {filename}", todesc=f"New Version: {filename}")

        # Save the diff HTML to the output folder
        output_file_path = os.path.join(output_folder, f'diff_{filename}.html')
        with open(output_file_path, 'w', encoding="utf-8") as output_file:
            output_file.write(diff_html)

    print("Comparison completed. HTML files saved to the output folder.")


###
old_folder = old_folder_path
new_folder = new_folder_path
output_folder = output_folder_path

compare_files_in_folders(old_folder, new_folder, output_folder)
compare_html_files_in_folders_bs4(old_folder, new_folder, f'{output_folder}/Overview.xlsx')