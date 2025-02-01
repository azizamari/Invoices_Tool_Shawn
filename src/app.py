import streamlit as st
import uuid
import os
import sys
import subprocess
from cogservice import extract_fields_from_invoice, generate_invoice_excel

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
    """Saves uploaded file to a safe temp directory and confirms it was saved."""
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

def open_excel_file(file_path, open_folder=False):
    """Opens the generated Excel file or its containing folder quickly."""
    try:
        if not os.path.exists(file_path):
            st.error(f"File not found: {file_path}")
            return

        if open_folder:
            folder_path = os.path.dirname(file_path)
            if sys.platform == "win32":
                os.startfile(folder_path)  
            elif sys.platform == "darwin":  
                subprocess.run(["open", folder_path])
            else:  
                subprocess.run(["xdg-open", folder_path])
        else:
            if sys.platform == "win32":
                os.startfile(file_path)  
            elif sys.platform == "darwin":  
                subprocess.run(["open", file_path])
            else:  
                subprocess.run(["xdg-open", file_path])
    except Exception as e:
        st.error(f"Could not open the file: {e}")

def main():
    # Hide Streamlit's UI components
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("Invoice Extraction Internal Tool")
    st.write("Drag and drop or browse an invoice (PDF), and the extracted data will be visualized.")

    # Initialize session state variables if they do not exist
    if "uploaded_file_path" not in st.session_state:
        st.session_state.uploaded_file_path = None
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None
    if "excel_file_path" not in st.session_state:
        st.session_state.excel_file_path = None
    if "previous_filename" not in st.session_state:
        st.session_state.previous_filename = None  # Store last uploaded filename

    uploaded_file = st.file_uploader("Upload your invoice (PDF)", type=["pdf"])

    # ✅ Reset state when a new file is uploaded
    if uploaded_file and uploaded_file.name != st.session_state.previous_filename:
        st.session_state.uploaded_file_path = None
        st.session_state.extracted_data = None
        st.session_state.excel_file_path = None
        st.session_state.previous_filename = uploaded_file.name  # Store new filename

    if uploaded_file and st.session_state.uploaded_file_path is None:
        st.write("Processing your invoice...")
        
        try:
            # Save uploaded file (only if not already uploaded)
            temp_filepath = save_uploaded_file(uploaded_file)
            
            if temp_filepath:
                st.session_state.uploaded_file_path = temp_filepath
                st.success(f"File successfully uploaded: `{temp_filepath}`")

                # Extract fields from invoice (only process once)
                extracted_data, invoice_text= extract_fields_from_invoice(temp_filepath)
                if extracted_data:
                    st.session_state.extracted_data = extracted_data

                    # Generate Excel and save path in state
                    temp_dir = get_temp_dir()
                    excel_path = generate_invoice_excel(extracted_data, invoice_text, temp_filepath)
                    st.session_state.excel_file_path = excel_path

                    st.success(f"Excel file saved at: `{excel_path}`")
                else:
                    st.error("No fields extracted.")
            else:
                st.error("Failed to save uploaded file.")

        except Exception as e:
            st.error(f"An error occurred while processing the invoice: {e}")

    # If processing is already done, show the results
    if st.session_state.excel_file_path:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Open Extracted Excel File"):
                open_excel_file(st.session_state.excel_file_path)

        with col2:
            if st.button("Open Containing Folder"):
                open_excel_file(st.session_state.excel_file_path, open_folder=True)

if __name__ == "__main__":
    main()
