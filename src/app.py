import streamlit as st
import uuid
import os
import io
from cogservice import extract_fields_from_invoice, generate_invoice_excel

def save_uploaded_file(uploaded_file):
    """
    Saves the uploaded file temporarily.
    """
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_filepath = os.path.join("temp_uploads", temp_filename)

    os.makedirs("temp_uploads", exist_ok=True)

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
        st.write("Processing your invoice...")

        try:
            # Save file and process extraction
            temp_filepath = save_uploaded_file(uploaded_file)
            result_dict = extract_fields_from_invoice(temp_filepath)

            if result_dict:
                # Display extracted fields
                # st.subheader("Extracted Invoice Data")
                # st.json(result_dict)

                # Generate Excel file for download
                excel_file = generate_invoice_excel(result_dict, uploaded_file.name)
                
                # Provide a download button
                st.download_button(
                    label="Download Extracted Data as Excel",
                    data=excel_file,
                    file_name="extracted_invoice_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:
                st.error("No fields extracted.")

            # Cleanup temp file
            os.remove(temp_filepath)

        except Exception as e:
            st.error(f"An error occurred while processing the invoice: {e}")

if __name__ == "__main__":
    main()
