# discord-bot-for-github

A small Discord bot that helps inspect and analyze GitHub repositories. The bot can fetch repository structure, file contents, contributors, and commit history using the GitHub API, and it can call an LLM (Azure OpenAI) to analyze or summarize repository or file content.

## Features

- Responds to simple chat messages (e.g., "hello").
- Basic commands and slash command example (`ping`).
- Repo inspection commands:
	- `!repo_structure <GitHub Repo URL>` — show directory tree for a repository.
	- `!contributors <GitHub Repo URL>` — list contributors.
	- `!commit_history <GitHub Repo URL>` — show recent commits.
	- `!file_content <GitHub Repo URL> <file path>` — fetch a file from the repo.
- AI-powered analysis (requires Azure OpenAI credentials):
	- `!wtfisthis <GitHub Repo URL>` — analyze repository structure and README.
	- `!wtfishappening <GitHub Repo URL> <file path>` — analyze a file's content.
	- `!summarizefile <GitHub Repo URL> <file path>` — summarize a file.

## Quickstart

Prerequisites

- Python 3.10+ installed on your machine.
- A Discord bot token (create a bot at the Discord Developer Portal and invite it to your server).
- A GitHub Personal Access Token with `repo` (or at least `public_repo`) access to read repository contents (if you access private repos, ensure the token has the right scopes).
- (Optional / for AI features) Azure OpenAI resource with a deployment and API key.

Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux (zsh)
pip install -r requirements.txt
```

Environment variables

Create a `.env` file in the project root with the following variables (example):

```
BOT_TOKEN=your_discord_bot_token_here
GITHUB_TOKEN=your_github_personal_access_token_here

# Azure OpenAI (optional, required for `llms.py` features)
AZURE_OPENAI_API_VERSION=2025-04-14
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

Running the bot

```bash
# from project root (with virtualenv activated)
python app.py
```

On successful startup you'll see a message like `Logged in as <botname>`. The bot will register a guild-scoped slash command (see `app.py`) — update the `guild` ID in `app.py` to your own server ID if you plan to use slash commands.

Procfile

This repo includes a `Procfile` which can be used for Heroku-style deployments. Example entry (already present in the repo):

```
web: python app.py
```

## Code Overview

- `app.py` — main Discord bot logic and the command handlers. This file wires commands to helper functions and streams outputs back to Discord channels or as text files when content is large.
- `githhub_script.py` — helpers that call the GitHub REST API to parse a repository URL, fetch directory contents, list contributors, get commit history, and retrieve file contents. Uses `GITHUB_TOKEN` from the environment.
- `llms.py` — wrapper functions for calling Azure OpenAI (chat completions) to analyze repository structure and file contents. Requires Azure OpenAI environment variables.
- `cleaning.py` — (utility) contains content post-processing helpers used to clean LLM output before sending to Discord.

## Commands & Usage Examples

Examples (in a Discord channel where the bot is present):

- Ping: `!ping` or use the `/ping` slash command.
- Say: `!say Hello world` — bot will repeat the message.
- Repo structure: `!repo_structure https://github.com/owner/repo`
- File content: `!file_content https://github.com/owner/repo path/to/file.py`
- Analyze repo with AI: `!wtfisthis https://github.com/owner/repo`

Notes

- Large outputs are truncated or sent as file attachments to avoid hitting Discord message length limits.
- Ensure `GITHUB_TOKEN` is set correctly and has permission to read the repository you query.

## Troubleshooting

- Bot doesn't respond / fails to start:
	- Verify `BOT_TOKEN` is set and correct.
	- Confirm the bot is invited to the server and has necessary permissions (send messages, read message history, use slash commands if used).
- GitHub API errors:
	- Check `GITHUB_TOKEN` and rate limits. If hitting rate limits, consider using a token with higher rate limits or caching results.
- Azure OpenAI errors for LLM commands:
	- Verify all `AZURE_*` variables are correct and the deployment name exists.

## Security and Privacy

- Do not commit your `.env` file or tokens to the repository.
- Tokens in environment variables grant access to services — rotate them if you suspect compromise.

## Contributing

Contributions are welcome. Open an issue or a pull request with a description of your change.

## Next steps / Ideas

- Add rate-limiting and caching for GitHub API calls.
- Add tests and CI configuration.
- Add a command permission system (only allow certain roles to call AI-intensive commands).

## License

This repository does not include a license file. If you plan to open-source it, add a `LICENSE` file (MIT, Apache-2.0, etc.).
