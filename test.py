import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    reader = PdfReader(pdf_path)

    # Check if the PDF has at least one page
    if len(reader.pages) > 0:
        # Extract text from the first page (index 0)
        first_page = reader.pages[0]
        text = first_page.extract_text()
        return text
    else:
        return None


pdf_text = extract_text_from_pdf("p.pdf")

user_input = input("Enter values you would like to extract")


# Call OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful data entry assistant. Extract the f{user_input} values out of provided pdf document and output in JSON format. Do not include newline characters and ensure the output is a single-line JSON string with clear key-value pairs."
        },
        {
            "role": "user",
            "content": pdf_text
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "general_document_response",
            "schema": {
                "type": "object",
                "properties": {
                    "documents": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "documentTitle": {
                                    "type": "string"
                                },
                                "content": {
                                    "type": "object",
                                    "properties": {
                                        "fields": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "additionalProperties": False
                                }
                            },
                            "required": ["documentTitle", "content"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["documents"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

# Clean up the response to remove newlines and format it correctly
response_text = response.choices[0].message.content
cleaned_response = response_text.replace('\n', '').strip()

# Load the cleaned response as JSON
response_json = json.loads(cleaned_response)

# Print the formatted JSON output
print(json.dumps(response_json, indent=2))

print(pdf_text)
