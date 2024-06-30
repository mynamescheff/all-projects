import openpyxl

def autofit_columns(file_path):
    # Load the workbook and select the active worksheet
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    # Iterate over all columns in the worksheet
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                # Determine the maximum length in the column
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        # Set the column width
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Save the workbook
    wb.save(file_path)
    print("Auto-fit columns operation completed.")


file_path = 'C:\\projects\\all-projects\\other\\excel_test\\test.xlsx'

# Call the function to autofit columns
autofit_columns(file_path)