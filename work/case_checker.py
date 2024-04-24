import os
from datetime import datetime
from openpyxl import load_workbook

class CaseList:
    def __init__(self, excel_folder, list_folder):
        self.excel_folder = excel_folder
        self.list_folder = list_folder

    def process_excel_files(self):
        list_file_path = os.path.join(self.list_folder, "list.txt")
        existing_values = {}
        unique_values = {}
        error_messages = []

        if os.path.isfile(list_file_path):
            existing_values = self.load_existing_list(list_file_path)

        for file_name in os.listdir(self.excel_folder):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(self.excel_folder, file_name)
                try:
                    wb = load_workbook(file_path)
                    sheet = wb.active
                    value = sheet["B17"].value

                    if value in existing_values:
                        existing_values[value] = True
                        unique_values[value] = file_name + " - DUPLICATE"
                    else:
                        existing_values[value] = False
                        unique_values[value] = file_name

                except Exception as e:
                    error_messages.append(f"Error processing file '{file_name}': {str(e)}")

        duplicate_values = [value for value, is_duplicate in existing_values.items() if is_duplicate]

        if unique_values:
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(list_file_path, "a", encoding="utf-8") as file:
                file.write(f"\n--- Updated on {today} ---\n")
                for value, file_name in unique_values.items():
                    file.write(f"{value} [{file_name}] ({today})\n")

        return duplicate_values, unique_values, error_messages

    def load_existing_list(self, list_file_path):
        existing_values = {}
        with open(list_file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and not line.startswith("---"):
                    value = line.split(" [")[0]
                    existing_values[value] = False
        return existing_values

# This setup allows for the functions to be directly called from a GUI handler
