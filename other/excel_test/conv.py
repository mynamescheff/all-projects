import openpyxl

def rename_duplicates(file_path, sheet_name):
    # Load the workbook and select the sheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]

    # Dictionary to keep track of the counts of each value
    value_counts = {}

    def rename_value(value):
        if value in value_counts:
            value_counts[value] += 1
            return f"{value}{value_counts[value]}"
        else:
            value_counts[value] = 0
            return value

    # Iterate through column A and rename duplicates
    for row in range(1, sheet.max_row + 1):
        cell_value = sheet[f'A{row}'].value
        if cell_value is not None:
            new_value = rename_value(cell_value)
            sheet[f'A{row}'] = new_value

    # Save the updated workbook
    workbook.save(file_path)

# Example usage
file_path = 'path_to_your_file.xlsx'
sheet_name = 'Sheet1'  # Change this to your actual sheet name if different
rename_duplicates(file_path, sheet_name)
