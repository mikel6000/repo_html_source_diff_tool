
import os
import pandas as pd
from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def compare_html_files_in_folders_bs4(folder1, folder2, output_excel):
    comparison_data = []

    # Get list of files in both folders
    folder1_files = set(os.listdir(folder1))
    folder2_files = set(os.listdir(folder2))
    
    # Find common files in both folders
    common_files = folder1_files.intersection(folder2_files)
    
    for file_name in common_files:
        file1_path = os.path.join(folder1, file_name)
        file2_path = os.path.join(folder2, file_name)
        
        # Extract text and compare
        html_text1 = extract_text_from_html(file1_path)
        html_text2 = extract_text_from_html(file2_path)
        comparison_result = "identical" if html_text1 == html_text2 else "differ"
        
        # Append result to comparison_data
        comparison_data.append({
            "Old_Version": file_name,
            "New_Version": file_name,
            "Comparison_Output": comparison_result
        })
    
    # Create a DataFrame from comparison_data
    df = pd.DataFrame(comparison_data)
    
    # Write DataFrame to an Excel file
    df.to_excel(output_excel, index=False)


# Compare files from 2 folders
# old_folder = 'C:/Users/michaeljohn.roguel/Desktop/checker_trial/old_pagesource_html_files'
# new_folder = 'C:/Users/michaeljohn.roguel/Desktop/checker_trial/new_pagesource_html_files'

# compare_html_files_in_folders_bs4(old_folder, new_folder, 'Result.xlsx')
# print('Comparing DONE!')

#--------------------------------------------------- START
# from bs4 import BeautifulSoup

# def extract_text_from_html(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, 'html.parser')
#         return soup.get_text()

# html_text1 = extract_text_from_html('old_test1.html')
# html_text2 = extract_text_from_html('new_test1.html')

# if html_text1 == html_text2:
#     print("The HTML files are identical.")
# else:
#     print("The HTML files differ.")
#--------------------------------------------------- END