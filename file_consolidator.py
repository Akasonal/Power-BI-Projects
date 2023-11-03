import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Define the app title and page layout
st.title("Finance File Consolidator")

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

    # Save consolidated data to an Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
        consolidated_data.to_excel(writer, index=False, sheet_name="Consolidated Data")

    # Create a download button for the consolidated Excel file
    download_link = st.empty()
    excel_file.seek(0)
    b64 = base64.b64encode(excel_file.read()).decode()
    download_link.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="consolidated_data.xlsx">Download Excel File</a>', unsafe_allow_html=True)
