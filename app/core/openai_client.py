from openai import OpenAI

from app.config import OPENAI_API_KEY
# client = OpenAI(api_key=OPENAI_API_KEY)

from langsmith.wrappers import wrap_openai

openai_client = OpenAI(api_key=OPENAI_API_KEY)
client = wrap_openai(openai_client)