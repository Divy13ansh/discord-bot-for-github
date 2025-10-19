import os
from dotenv import load_dotenv
load_dotenv()

print("GITHUB_TOKEN:", os.getenv("GITHUB_TOKEN"))
print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("AZURE_OPENAI_ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("AZURE_API_KEY:", os.getenv("AZURE_API_KEY"))
print("AZURE_OPENAI_DEPLOYMENT:", os.getenv("AZURE_OPENAI_DEPLOYMENT"))
print("AZURE_OPENAI_API_VERSION:", os.getenv("AZURE_OPENAI_API_VERSION"))