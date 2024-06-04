#write a function that will check if a name of the file is the same (or like 90% similar) to a string in C20 cell in each excel file in the folder

import openpyxl
import os
import difflib
import pandas as pd

def similar(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


# Define the path to the folder containing the Excel files
folder_path = r"your_folder_path"

# Create a list of all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Create a DataFrame to store the results
df = pd.DataFrame(columns=['File', 'Sheet', 'Name', 'C20'])

# Loop through all Excel files in the folder
for excel_file in excel_files:
    # Load the Excel file
    wb = openpyxl.load_workbook(os.path.join(folder_path, excel_file))
    # Loop through all worksheets in the file
    for sheet in wb.worksheets:
        # Get the C20 cell value
        c20_cell = sheet["C20"].value
        if c20_cell is not None:
            # Loop through all other worksheets in the file
            for other_sheet in wb.worksheets:
                if other_sheet != sheet:
                    # Get the name cell value
                    name_cell = other_sheet["B1"].value
                    if name_cell is not None:
                        # Check if the name cell value is similar to the C20 cell value
                        if similar(name_cell, c20_cell) > 0.9:
                            # Append the results to the DataFrame
                            df = df.append({'File': excel_file, 'Sheet': sheet.title, 'Name': name_cell, 'C20': c20_cell}, ignore_index=True)



# The function similar() calculates the similarity ratio between two strings using the difflib library.
# If the ratio is greater than 0.9, the function returns True. Otherwise, it returns False.
# The script then loops through all files in the specified folder and checks if each file is an Excel file.
# For each Excel file, it loops through all worksheets in the file and checks if the C20 cell value is not None.
# If the C20 cell value is not None, it loops through all other worksheets in the file and checks if the name cell value is not None.
# If the name cell value is similar to the C20 cell value, it prints the file name, sheet name, name cell value, and C20 cell value.
# The script uses the openpyxl library to load and manipulate Excel files, and the os library to work with file paths.
# The script can be modified to handle different file structures and requirements based on specific needs.

"""from fuzzywuzzy import fuzz
import os

def check_file_names(folder_path, target_string):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if fuzz.partial_ratio(target_string, file) >= 90:
                print(f"Match found: {file} in {root}")"""