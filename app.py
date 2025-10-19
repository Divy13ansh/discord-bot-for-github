import discord
from discord.ext import commands
from githhub_script import get_repo_structure, repo_dict, get_contributors
from llms import analyze_repository_structure
import os
from dotenv import load_dotenv
import io

load_dotenv()

# Intents are required to specify what events your bot can receive
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

# Prefix for bot commands (like !ping)
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: When bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# Event: When someone sends a message
@bot.event
async def on_message(message):
    # Prevent bot from replying to itself
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        await message.channel.send(f"Hey {message.author.name}! 👋")

    # Allow command processing to still happen
    await bot.process_commands(message)

# Command example: !ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

# Command example: !say <message>
@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def helpme(ctx):
    help_text = """
    **Available Commands:**
    `!ping` - Check if the bot is responsive.
    `!say <message>` - Make the bot repeat your message.
    `!repo_structure <GitHub Repo URL>` - Fetch and display the directory structure of a GitHub repository.
    """
    await ctx.send(help_text)

@bot.command()
async def repo_structure(ctx, *, url):
    """Fetch and display the directory structure of a GitHub repository."""
    if url is None:
        await ctx.send("Please provide a GitHub repository URL.")
        return
    structure = get_repo_structure(url)

    max_length = 1900  # leave space for formatting
    output = str(structure)
    if len(output) > max_length:
        file = io.StringIO(output)
        output = output[:max_length] + "\n... (truncated)"
        await ctx.send("Repository structure is too long, sending as a file:", file=discord.File(file, filename="repo_structure.txt"))
    else:
        await ctx.send(f"Repository Structure:\n```{output}```")

@bot.command()
async def wtfisthis(ctx, *, repository_url):
    """Uses AI to tell you whats going on in this repo"""
    # Placeholder for AI integration
    structure = get_repo_structure(repository_url)
    analysis = analyze_repository_structure(structure)
    file = io.StringIO(analysis)
    await ctx.send(f"Analysis of the repository:\n", file=discord.File(file, filename="repo_analysis.md"))

@bot.command()
async def contributors(ctx, *, repo_url):
    """Fetch and display the list of contributors for a given GitHub repository URL."""
    try:
        contributors = get_contributors(repo_url)
        if not contributors:
            await ctx.send("No contributors found for this repository.")
            return

        contributor_list = "\n".join([f"- {contributor}" for contributor in contributors])
        if len(contributor_list) > 1900:
            file = io.StringIO(contributor_list)
            await ctx.send("Contributor list is too long, sending as a file:", file=discord.File(file, filename="contributors.txt"))
        else:
            await ctx.send(f"**Contributors:**\n{contributor_list}")
    except Exception as e:
        await ctx.send(f"An error occurred while fetching contributors: {str(e)}")

# Run your bot
bot.run(str(os.getenv("BOT_TOKEN")))