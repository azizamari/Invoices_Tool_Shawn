import streamlit as st
import uuid
import os
import sys
import subprocess
import dotenv

from cogservice import extract_fields_from_invoice, generate_invoice_excel
from batch_cogservice import batch_extract_fields_from_invoices, generate_batch_invoices_excel

def check_and_prompt_env_vars():
    required_vars = [
        "DOCUMENT_INTELLIGENCE_API_KEY",
        "DOCUMENT_INTELLIGENCE_ENDPOINT",
        "AZURE_URL",
        "AZURE_API_KEY"
    ]
    
    dotenv_path = ".env"
    dotenv.load_dotenv(dotenv_path)
    
    env_values = {}
    st.subheader("Modify Environment Variables")
    for var in required_vars:
        env_values[var] = st.text_input(f"Enter {var}", value=os.getenv(var, ""), type="password")
    
    if st.button("Save and Reload"):
        with open(dotenv_path, "w") as f:
            for key, value in env_values.items():
                if value:
                    f.write(f"{key}={value}\n")
        
        st.success("Environment variables saved. Please restart the app.")
        st.stop()
    print(env_values)
    return env_values

def get_temp_dir():
    """Returns the correct temp directory, even when running as an .exe"""
    if getattr(sys, 'frozen', False):  # If running as an EXE
        base_path = sys._MEIPASS  # PyInstaller extracts files here
    else:
        base_path = os.getcwd()  # Normal script execution

    temp_path = os.path.join(base_path, "temp_uploads")
    os.makedirs(temp_path, exist_ok=True)
    return temp_path

def save_uploaded_file(uploaded_file):
    """Saves an uploaded file to a safe temp directory and returns the file path."""
    try:
        temp_dir = get_temp_dir()
        os.makedirs(temp_dir, exist_ok=True)
        temp_filename = f"{uuid.uuid4()}.pdf"
        temp_filepath = os.path.join(temp_dir, temp_filename)
        file_data = uploaded_file.getvalue()
        with open(temp_filepath, "wb") as f:
            f.write(file_data)

        if os.path.exists(temp_filepath):
            return temp_filepath
        else:
            st.error(f"File save failed: `{temp_filepath}` does not exist!")
            return None
    except Exception as e:
        st.error(f"An error occurred while saving the uploaded file: {e}")
        return None

def main():
    config = check_and_prompt_env_vars()
    
    if not all(config.values()):
        st.error("All required environment variables must be set before uploading data.")
        return
    
    st.title("Invoice Extraction Internal Tool")
    st.write("Select a processing mode below:")
    
    mode = st.radio("Select Processing Mode", ["Single Invoice", "Batch Invoices"])
    
    if mode == "Single Invoice":
        st.subheader("Single Invoice Processing")
        uploaded_file = st.file_uploader("Upload your invoice (PDF)", type=["pdf"])
        
        if uploaded_file:
            temp_filepath = save_uploaded_file(uploaded_file)
            if temp_filepath:
                extracted_data, invoice_text = extract_fields_from_invoice(temp_filepath, config=config)
                if extracted_data:
                    excel_path = generate_invoice_excel(extracted_data, invoice_text, temp_filepath, config=config)
                    st.success(f"Excel file saved at: `{excel_path}`")
    
    else:  # Batch Invoices mode
        st.subheader("Batch Invoices Processing")
        uploaded_files = st.file_uploader("Upload invoice PDFs", type=["pdf"], accept_multiple_files=True)
        
        if uploaded_files:
            batch_file_paths = [save_uploaded_file(file) for file in uploaded_files if file]
            if batch_file_paths:
                batch_results = batch_extract_fields_from_invoices(batch_file_paths, config=config, parallel=True)
                batch_excel = generate_batch_invoices_excel(batch_results, config=config)
                st.success(f"Batch processing complete. Excel file saved at: `{batch_excel}`")

if __name__ == "__main__":
    main()
