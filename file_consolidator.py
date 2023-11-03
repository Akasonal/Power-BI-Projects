import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Define the app title and page layout
st.title("Finance File Consolidator")

# Function to create a download link for a binary file
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="consolidated_data.xlsx">Download Excel File</a>'
    return href

# Upload multiple Excel files
uploaded_files = st.file_uploader("Upload multiple Excel files (xlsx)", type=["xlsx"], accept_multiple_files=True)

consolidated_data = pd.DataFrame()  # Initialize an empty DataFrame to consolidate data

# Function to read and concatenate data
def read_and_concat_data(files, sheet_name):
    total_files = len(files)
    data_frames = []  # Initialize a list to store DataFrames from individual files
    for i, file in enumerate(files):
        data = pd.read_excel(file, sheet_name=sheet_name, header=1)
        data_frames.append(data)
        # Calculate progress
        progress = (i + 1) / total_files
        st.progress(progress)
    consolidated_data = pd.concat(data_frames, ignore_index=True)
    return consolidated_data

if uploaded_files:
    consolidated_data = read_and_concat_data(uploaded_files, '1.FinanceAllOrderNewDP Base')

    # Display data overview in the main page
    st.header("Data Overview")
    st.write(consolidated_data)  # Display the data overview on the main page

    # Create a progress bar for the data overview
    progress_bar = st.progress(0)  # Initialize the progress bar

    # Update the progress bar
    for i in range(100):
        progress_bar.progress((i + 1) / 100)
    
    # Save consolidated data to an Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
        consolidated_data.to_excel(writer, index=False, sheet_name="Consolidated Data")

    # Create a download button for the consolidated Excel file
    st.markdown(get_binary_file_downloader_html(excel_file, "Download Excel File"), unsafe_allow_html=True)
