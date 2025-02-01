from pydantic import BaseModel, Field
from typing import Optional
from model_hub.llm_factory import LLMFactory

class InvoiceDetails(BaseModel):
    expense_type: str = Field(description="Type of expense: Rental, Material, Site Expenses, Reimbursement, Other")
    approval: str = Field(description="Approval status of the invoice: Approved, Denied, Not Specified")
    job_location: Optional[str]= Field(default='', description="Job site name or job number if available, job site is not a company")



def extract_invoice_details(invoice_text: str, extracted_fields):
    messages = [
        {"role": "system", "content": "You are an expert in extracting structured information from a contructions company's invoices with high accuracy."},
        {
            "role": "user",
            "content": (
                "You are provided with raw invoice text extracted through OCR.\n"
                f"### Raw Invoice Text:\n{invoice_text}\n"
                f"### Some of the fields I already extracted:\n{extracted_fields}\n"
                "### Important Instructions:\n"
                "1. **Only extract information if you are certain about its accuracy.** If a field cannot be determined with confidence, return an empty value.\n"
                "2. **Do not confuse job site/address with vendor or customer name.** The job location refers to the worksite or project location, not billing/shipping details.\n"
            )
        }
    ]
    llm = LLMFactory(provider="azure")
    completion = llm.create_completion(
        response_model=InvoiceDetails,
        messages=messages,
    )
    return completion.model_dump()