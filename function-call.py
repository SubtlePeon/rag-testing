import google.generativeai as genai
import logging
import os
import requests

from dotenv import find_dotenv, load_dotenv
from custom_types.nytimes import BookResponse

lg = logging.getLogger(__name__)
logging.basicConfig(
    format = "%(name)s - %(levelname)s: %(message)s",
    level = logging.INFO,
)

_ = load_dotenv(find_dotenv())
if "GOOGLE_API_KEY" not in os.environ:
    raise Exception(
        "Couldn't find `GOOGLE_API_KEY` environmental variable (or in `.env`)"
    )
genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

# Tool delarations
tools = [
    genai.protos.FunctionDeclaration(
        name = "get_books",
        description = "Get some books from NY Times",
        parameters = genai.protos.Schema(
            type = genai.protos.Type.NUMBER
        ),
    ),
]

class Tools:
    @staticmethod
    def get_books() -> BookResponse:
        """Gets some hardcover fiction from NY Times' API."""
        lg.info("func-call: get_books")
        resp = requests.get(
            "https://api.nytimes.com/svc/books/v3/lists/current/" +
            f"hardcover-fiction.json?api-key={os.environ['NYT_API_KEY']}"
        )
        return resp.json()

model = genai.GenerativeModel(
    model_name = "models/gemini-1.5-pro-latest",
    tools = [Tools.get_books],
)
chat = model.start_chat(enable_automatic_function_calling = True)
response = chat.send_message(
    "Can you get some books from NY Times for me?",
)

for part in response.candidates[0].content.parts:
    if "text" in part:
        print(part.text)
    else:
        lg.warn(f"Unknown part: {part}")
