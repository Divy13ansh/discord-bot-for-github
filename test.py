import os
from dotenv import load_dotenv
load_dotenv()

print("GITHUB_TOKEN:", os.getenv("GITHUB_TOKEN"))
print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))