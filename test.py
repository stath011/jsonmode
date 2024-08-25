import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Example PDF text (normally, you would extract this from an actual PDF)
pdf_text = """
Product data sheet
Specifications
Wear part, fan for soft starter,
subassembly, Altistar 22, 110V, size
E
VZ3V22E1110V
Main
Range compatibility Altistar 22
Accessory / separate part type Fan kit
Accessory / separate part
category
Cooling accessory
Product or component type Fan
Complementary
Kit composition Fan
Mounting bracket
Instruction sheet
Compatibility with soft starter Soft starter ATS22 110...115 V (size: 304 x 340 x 455 mm)
Accessory / separate part
destination
Soft starter
Packing Units
Unit Type of Package 1 PCE
Number of Units in Package 1 1
Package 1 Height 11.500 cm
Package 1 Width 30.000 cm
Package 1 Length 40.000 cm
Package 1 Weight 2.192 kg
Unit Type of Package 2 P06
Number of Units in Package 2 10
Package 2 Height 75.000 cm
Package 2 Width 60.000 cm
Package 2 Length 80.000 cm
Package 2 Weight 34.920 kg
Recommended replacement(s)
Disclaimer: This documentation is not intended as a substitute for and is not to be used for determining suitability or reliability of these products for specific user applications
Jan 18, 2023 1
"""

# Call OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful data entry assistant. Extract the relevant values out of provided pdf documents and output in JSON format. Do not include newline characters and ensure the output is a single-line JSON string with clear key-value pairs."
        },
        {
            "role": "user",
            "content": pdf_text
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document_response",
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
