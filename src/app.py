import streamlit as st
import uuid
import os
from cogservice import extract_fields_from_invoice

def save_uploaded_file(uploaded_file):
    # Generate a temporary file path with a UUID name
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_filepath = os.path.join("temp_uploads", temp_filename)

    # Ensure the directory exists
    os.makedirs("temp_uploads", exist_ok=True)

    # Save the file to the temporary path
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.read())
    
    return temp_filepath

def main():
    # Hide Streamlit's default UI components
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # App title
    st.title("Invoice Extraction Internal Tool")
    st.write("Drag and drop or browse an invoice (PDF), and the extracted data will be visualized.")

    # File uploader for invoices
    uploaded_file = st.file_uploader("Upload your invoice (PDF)", type=["pdf"])
    
    if uploaded_file is not None:
        st.write("Processing your invoice...")  # Display while processing

        # Save the uploaded file to disk
        try:
            temp_filepath = save_uploaded_file(uploaded_file)

            # Process the saved file
            result_dict = extract_fields_from_invoice(temp_filepath)

            # Display the result as a dictionary
            st.subheader("Extracted Invoice Data")
            st.json(result_dict)

            # Clean up: Delete the temporary file after processing
            os.remove(temp_filepath)

        except Exception as e:
            st.error(f"An error occurred while processing the invoice: {e}")

if __name__ == "__main__":
    main()
