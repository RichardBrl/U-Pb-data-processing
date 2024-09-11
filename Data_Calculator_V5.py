import streamlit as st
st.title('Data Calculator V5')

import pandas as pd
from pyxlsb import open_workbook
import openpyxl
from tqdm.auto import tqdm # Ladebalken, optional
import re

input_file = r'./input_files/2024-05-25 Seq1 All csv.xlsb'
output_file = r'./output_files/StatDat_.xlsx'

#Gewünschte Einstellungen. Default-Einstellungen wurden vorgegeben
skip_first_channel = input(f"Skip first channel if saturated? (yes/no) [default: yes]: ").strip().lower() or "yes"
min_cps = int(input(f"Minimum CPS to calculate ACF [default: 500000]: ") or 500000)
max_cps = int(input(f"Maximum CPS to calculate ACF for [default: 50000000]: ") or 50000000)

#Sheet-Namen speichern, wird für die Output-Datei benötigt
with open_workbook(input_file) as wb:
    sheet_names = wb.sheets

