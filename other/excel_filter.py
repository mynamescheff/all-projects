import pandas as pd
import os

def filter_and_save_excel(input_file):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load the Excel file
    df = pd.read_excel(input_file, header=None)

    # Copy rows 1 to 6 and row 10
    header_rows = df.iloc[list(range(6)) + [9], :16]

    # Iterate over each row starting from row 11
    for index, row in df.iloc[10:, :].iterrows():
        if pd.notnull(row[4]):  # Check if column E (index 4) is not empty
            new_filename = f"{row[4]}.xlsx"

            # Create a new DataFrame for this specific row
            filtered_row = row[:16].to_frame().transpose()

            # Combine header rows with the filtered row
            combined_df = pd.concat([header_rows, filtered_row], ignore_index=True)

            # Define the full path for the new file
            new_file_path = os.path.join(script_dir, new_filename)

            # Save to a new Excel file
            with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
                combined_df.to_excel(writer, index=False, header=False)

# Usage
input_file = 'your_input_file.xlsx'  # Replace with your actual file name
filter_and_save_excel(input_file)
