import streamlit as st
st.title('Data Calculator V5')

import pandas as pd
from pyxlsb import open_workbook
import openpyxl
from tqdm.auto import tqdm # Ladebalken, optional
import re

input_file = r'./input_files/2024-05-25 Seq1 All csv.xlsb'
output_file = r'./output_files/StatDat_.xlsx'
