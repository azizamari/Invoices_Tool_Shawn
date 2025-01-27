import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOCUMENT_INTELLIGENCE_API_KEY")

if not endpoint or not key:
    raise ValueError("DOCUMENTINTELLIGENCE_ENDPOINT and DOCUMENTINTELLIGENCE_API_KEY must be set in .env.")

client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def extract_fields_from_invoice(file_path):
    """
    Extract specified fields from an invoice using Azure Document Intelligence.

    Args:
        file_path (str): Path to the invoice file.

    Returns:
        dict: Extracted fields with their values and confidence levels.
    """
    try:
        fields_to_extract = {
            "Vendor Name": "VendorAddressRecipient",
            "Customer Name": "CustomerAddressRecipient",
            "Date": "InvoiceDate",
            "Project Name": "ProjectName", 
            "Total Value": "InvoiceTotal",
            "Invoice Number": "InvoiceId"
        }
        with open(file_path, "rb") as document:
            poller = client.begin_analyze_document(
                model_id="prebuilt-invoice",
                body=document,
                features=[DocumentAnalysisFeature.QUERY_FIELDS],
                query_fields=[*list(fields_to_extract.values())],
            )
            result = poller.result()
        
        
        extracted_data = {}

        if result.documents:
            for document in result.documents:
                for field_name, model_field in fields_to_extract.items():
                    field = document.fields.get(model_field)
                    if field:
                        if model_field == "InvoiceTotal":
                            extracted_data[field_name] = {
                                "value": str(field.value_currency.amount) + " " + field.value_currency.currency_code,
                                "confidence": field.confidence
                            }
                        elif model_field == "InvoiceDate":
                            extracted_data[field_name] = {
                                "value": field.value_date,
                                "confidence": field.confidence
                            }
                        else:
                            extracted_data[field_name] = {
                                "value": field.content,
                                "confidence": field.confidence
                            }
        
        return extracted_data

    except HttpResponseError as e:
        print(f"An error occurred: {e.message}")
        return None

if __name__ == "__main__":
    invoice_file_path = r"D:\work\upwork\armstrong\FON-4245485-0002 ACB110.pdf"
    # invoice_file_path = r"D:\work\upwork\armstrong\2168515 ACB110.pdf"

    if not os.path.exists(invoice_file_path):
        raise FileNotFoundError(f"File not found: {invoice_file_path}")

    print(f"Analyzing invoice: {invoice_file_path}")

    extracted_fields = extract_fields_from_invoice(invoice_file_path)

    if extracted_fields:
        print("\nExtracted Fields:")
        for field, details in extracted_fields.items():
            print(f"{field}: {details['value']} (Confidence: {details['confidence']:.2f})")
    else:
        print("No fields extracted.")
