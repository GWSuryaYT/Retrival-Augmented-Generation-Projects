from dotenv import load_dotenv
import os

def api_giver():

    load_dotenv()

    api = os.getenv("GEMINI_API_KEY")

    return api

