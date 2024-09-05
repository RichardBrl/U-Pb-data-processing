import streamlit as st
st.title('Data Calculator V5')

import pandas as pd
from pyxlsb import open_workbook
import openpyxl
from tqdm import tqdm  # Import tqdm for the progress bar

input_file = r'./input_files/2024-05-25 Seq1 All csv.xlsb'
output_file = r'./output_files/StatDatResults_test3.xlsx'

with open_workbook(input_file) as wb:
    sheet_names = wb.sheets

def calculate_averages(sheet_name):
    # Read the input sheet
    df = pd.read_excel(input_file, sheet_name=sheet_name, engine='pyxlsb')
    
    # Extract the 'Time' column
    time_column = df.get('Time', None)  # Get the "Time" column if it exists

    # Initialize the dictionary for averages
    averages = {}
    
    # Extract base headers and print them
    base_headers = df.columns.str.extract(r'(^[a-zA-Z0-9_]+)')[0].unique()
   #print(base_headers)

    # Use tqdm to display progress for the loop
    for header in tqdm(base_headers, desc=f'Processing sheet: {sheet_name}'):
        if "Mass" in header and header.endswith('p'):
            base = header[:-1]
            mass_columns = df.filter(regex=fr'^{base}p(\.\d+)?$')
            acf_column = df.filter(regex=r'^ACF$')
            
            if not mass_columns.empty and not acf_column.empty:
                acf_values = acf_column.squeeze()
                average_list = []
                acf = []
                for i, row in mass_columns.iterrows():
                    if row.astype(str).str.contains(r'\*').any():
                        related_a_columns = df.filter(regex=fr'^{base}a(\.\d+)?$')
                        acf.append(None)
                        if not related_a_columns.empty:
                            cleaned_row = related_a_columns.loc[i].astype(str).str.replace('*', '').astype(float)
                            avg = (cleaned_row * acf_values.loc[i]).mean(skipna=True)
                            average_list.append(avg)
                        else:
                            average_list.append(None)
                    else:
                        avg = row.astype(float).mean(skipna=True)
                        average_list.append(avg)
                        related_a_columns = df.filter(regex=fr'^{base}a(\.\d+)?$')
                        if not related_a_columns.empty:
                            cleaned_row = related_a_columns.loc[i].astype(str).str.replace('*', '').astype(float)
                            avg_a = (cleaned_row * acf_values.loc[i]).mean(skipna=True)
                            #print(f'{avg}/{avg_a}')
                            if float(avg_a) != 0.0 and float(avg) != 0.0:
                                acf.append((float(avg) / float(avg_a))*64)
                            else:
                                acf.append(None)
                        else:
                            acf.append(None)
                averages[base] = average_list
                averages[f'ACF-{base}'] = acf

    # Convert the averages dictionary to DataFrame
    result_df = pd.DataFrame(averages)
    
    # Insert the 'Time' column as the first column if it exists
    if time_column is not None:
        result_df.insert(0, 'Time', time_column)
    
    return result_df

# Initialize an empty dictionary to hold the results
result_sheets = {}
for sheet_name in tqdm(sheet_names):
    result_sheets[sheet_name] = calculate_averages(sheet_name)

# Write results to Excel
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for sheet_name, result_df in result_sheets.items():
        if not result_df.empty:  # Write only non-empty DataFrames
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)
