import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")

)

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
              {"role": "user", "content": "how can I solve 8x + 7 = -23"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "steps",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

print(response.choices[0].message.content)
