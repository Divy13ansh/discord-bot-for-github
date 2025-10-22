import discord
from discord.ext import commands
from githhub_script import get_repo_structure, repo_dict, get_contributors, get_commit_history, get_file_content
from llms import analyze_repository_structure, analyze_file_content, summarize_file_content
from cleaning import clean_md_content
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
    `!wtfisthis <GitHub Repo URL>` - Analyze the repository structure using AI and provide insights.
    `!contributors <GitHub Repo URL>` - Fetch and display the list of contributors for a given GitHub repository.
    `!commit_history <GitHub Repo URL>` - Fetch and display the commit history for a given GitHub repository.
    `!file_content <GitHub Repo URL> <file path>` - Fetch and display the content of a specific file from a GitHub repository.
    `!wtfishappening <GitHub Repo URL> <file path>` - Analyze the content of a specific file in a GitHub repository using AI.
    `!summarizefile <GitHub Repo URL> <file path>` - Summarize the content of a specific file in a GitHub repository using AI.
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
    readme_content = get_file_content(repository_url, "README.md")
    repo_structure = f"README.md content:\n{readme_content}\n\nDirectory structure:\n{structure}"
    analysis = analyze_repository_structure(repo_structure)
    analysis = clean_md_content(analysis)
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

@bot.command()
async def commit_history(ctx, *, repo_url):
    """Fetch and display the commit history for a given GitHub repository URL."""
    try:
        commits = get_commit_history(repo_url)
        if not commits:
            await ctx.send("No commits found for this repository.")
            return

        commit_lines = [f"- {commit['sha'][:7]} by {commit['author']} on {commit['date']}: {commit['message']}" for commit in commits]
        commit_history_str = "\n".join(commit_lines)

        if len(commit_history_str) > 1900:
            file = io.StringIO(commit_history_str)
            await ctx.send("Commit history is too long, sending as a file:", file=discord.File(file, filename="commit_history.txt"))
        else:
            await ctx.send(f"**Commit History:**\n{commit_history_str}")
    except Exception as e:
        await ctx.send(f"An error occurred while fetching commit history: {str(e)}")

@bot.command()
async def file_content(ctx, repo_url, file_path):
    """Fetch and display the content of a specific file from a GitHub repository."""
    try:
        content = get_file_content(repo_url, file_path)
        await ctx.send(f"Content of `{file_path}` from `{repo_url}`:\n```{content}```")
    except Exception as e:
        await ctx.send(f"An error occurred while fetching file content: {str(e)}")

@bot.command()
async def wtfishappening(ctx, repo_url, file_path):
    """Analyze the content of a specific file in a GitHub repository using AI."""
    try:
        content = get_file_content(repo_url, file_path)
        analysis = analyze_file_content(f"{content}, file path: {file_path}")
        analysis = clean_md_content(analysis)
        file = io.StringIO(analysis)
        await ctx.send(f"Analysis of the file `{file_path}`:\n", file=discord.File(file, filename="file_analysis.md"))
    except Exception as e:
        await ctx.send(f"An error occurred while analyzing the file: {str(e)}")

@bot.command()
async def summarizefile(ctx, repo_url, file_path):
    """Summarize the content of a specific file in a GitHub repository using AI."""
    try:
        content = get_file_content(repo_url, file_path)
        summary = summarize_file_content(f"{content}, file path: {file_path}")
        summary = clean_md_content(summary)
        await ctx.send(f"Summary of the file `{file_path}`:\n {summary}")
    except Exception as e:
        await ctx.send(f"An error occurred while summarizing the file: {str(e)}")

# Run your bot
bot.run(str(os.getenv("BOT_TOKEN")))