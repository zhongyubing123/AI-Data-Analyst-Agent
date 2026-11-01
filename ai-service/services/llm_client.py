import os

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(ENV_PATH)



client = OpenAI(

    api_key=os.getenv("DEEPSEEK_API_KEY"),

    base_url="https://api.deepseek.com",

    timeout=60.0,

    max_retries=1

)