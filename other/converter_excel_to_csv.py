import openpyxl
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def trim_column_b_value(value, length):
    # Strip leading spaces and remove hyphens, then trim the string from column B to a maximum of 'length' characters
    value = value.lstrip().replace('-', '').replace('–', '')
    if len(value) <= length:
        return value
    else:
        trimmed = value[:length]
        last_space = trimmed.rfind(' ')
        if last_space != -1 and last_space < length - 1:
            next_word = value[last_space+1:].split()[0] if ' ' in value[last_space+1:] else value[last_space+1:]
            remaining_word_length = len(trimmed[last_space+1:])
            next_word_length = len(next_word)
            if remaining_word_length < next_word_length / 2:
                return trimmed[:last_space]
        return trimmed

def split_b_value(b_value):
    # Split the B value into chunks of up to 35 characters
    parts = []
    while len(b_value) > 35:
        split_point = 35
        while split_point > 0 and not b_value[split_point].isalnum():
            split_point -= 1
        if split_point == 0:
            split_point = 35  # In case no alphanumeric character is found
        parts.append(b_value[:split_point].rstrip())
        b_value = b_value[split_point:].lstrip()
    parts.append(b_value)
    return parts

def remove_duplicates(b_value):
    words = b_value.split()
    seen = set()
    result = []
    for word in words:
        if word not in seen:
            seen.add(word)
            result.append(word)
    return ' '.join(result)

def adjust_length(b_value, c_value):
    total_length = len(b_value) + len(c_value)
    if total_length <= 140:
        return b_value, c_value

    b_words = b_value.split()
    while len(' '.join(b_words)) + len(c_value) > 140:
        if len(b_words) > 1:
            b_words.pop()
        else:
            break
    return ' '.join(b_words), c_value

def determine_currency_bank_acc(currency):
    if currency in ["EUR", "USD", "CHF"]:
        return f"{currency} bank acc"
    else:
        return "GBP bank acc"

try:
    # Load the workbook and select the sheet
    workbook_path = 'C:\\IT project3\\utils\\combined_file.xlsx'
    logging.info(f'Loading workbook from {workbook_path}')
    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook['Transposed']
    logging.info('Workbook loaded successfully')

    # Specify the columns you want to extract
    columns = ['B', 'C', 'D', 'E', 'F', 'G', 'I']
    logging.debug(f'Columns to extract: {columns}')

    # Open a CSV file to write to
    csv_path = 'C:\\IT project3\\utils\\output.csv'
    logging.info(f'Opening CSV file at {csv_path} for writing')
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Iterate over the rows in the sheet
        for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row):
            # Check if the first cell in the row is empty, indicating the end of data
            if row[0].value is None:
                logging.info('Empty cell found in first column, stopping iteration')
                break

            # Extract and process values from columns B and C
            col_b_value = row[sheet['B1'].column - 1].value or ''
            col_c_value = row[sheet['C1'].column - 1].value or ''
            col_e_value = row[sheet['E1'].column - 1].value or ''

            # Process the B value
            trimmed_b_16 = trim_column_b_value(col_b_value, 16)
            b_parts = split_b_value(col_b_value)
            if len(b_parts) > 3:
                b_value = remove_duplicates(col_b_value)
                b_parts = split_b_value(b_value)
            
            # Ensure there are exactly three parts for the B value
            while len(b_parts) < 3:
                b_parts.append('')

            # Add the C value at the end of B parts
            b_parts.append(col_c_value)
            
            # Extract other column values
            other_values = [row[sheet[column + '1'].column - 1].value for column in columns[2:]]
            
            # Determine the currency bank account value
            currency_bank_acc = determine_currency_bank_acc(col_e_value)

            # Combine all values to write to the CSV
            row_data = [trimmed_b_16] + b_parts + other_values + [currency_bank_acc]
            logging.debug(f'Writing row data: {row_data}')
            # Write the row to the CSV file
            writer.writerow(row_data)
    
    logging.info('Data successfully written to CSV file')

except Exception as e:
    logging.error(f'An error occurred: {e}', exc_info=True)
