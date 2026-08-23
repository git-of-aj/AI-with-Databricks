# config/openai_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_openai_client() -> OpenAI:
    endpoint = os.getenv("ENDPOINT")
    api_key = os.getenv("API_KEY")

    if not endpoint:
        raise ValueError("ENDPOINT is not set.")

    if not api_key:
        raise ValueError("API_KEY is not set.")

    return OpenAI(
        base_url=endpoint,
        api_key=api_key,
    )
