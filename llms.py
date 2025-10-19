import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import re
load_dotenv()

api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # e.g., "2025-04-14"
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g., "https://subscription_key = os.getenv("AZURE_API_KEY")  # your API key
subscription_key = os.getenv("AZURE_API_KEY")  # your API key
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


# --------------------------
# Azure OpenAI config
# --------------------------
  # e.g., "https://YOUR_RESOURCE_NAME.openai.azure.com/"
  # latest supported version

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # your deployment name

# --------------------------
# Chat request
# --------------------------

def analyze_repository_structure(repo_structure):
    """Use Azure OpenAI to analyze the repository structure and provide insights."""
    response = client.chat.completions.create(
        model=deployment_name,  # deployment name
        messages=[
            {
                "role": "system",
                "content": """You are an expert software architect and repository analyst.

            Your task is to analyze the given directory structure of a project and infer as much as possible about the project’s purpose, technologies, and design. 
            You will receive a JSON-like or tree-style directory representation of a code repository.

            Your output must be a clear, structured summary covering the following points (even if some are uncertain — infer or note as unknown):

            1. **Project Overview:**  
            - What the project likely does or aims to achieve.  
            - The kind of software it is (e.g., web app, CLI tool, AI/ML model, SDK, library, etc.).

            2. **Primary Language(s) & Frameworks:**  
            - Identify the main programming language(s).  
            - Guess likely frameworks, libraries, or stacks (e.g., React, FastAPI, Django, Flask, Express, etc.).

            3. **Key Components / Architecture:**  
            - Describe the main modules and what roles they might play (e.g., `routes/`, `models/`, `services/`, etc.).  
            - Note architectural style (e.g., MVC, modular, layered, microservices, monorepo).

            4. **Build, Dependency & Config Management:**  
            - What build/dependency tools are used (e.g., `package.json`, `pyproject.toml`, `requirements.txt`, `Makefile`, `Dockerfile`)?  
            - Is there evidence of containerization or environment management?

            5. **Testing & Quality:**  
            - Presence of tests or CI/CD workflows.  
            - Likely testing framework(s).  
            - Code quality indicators (linting, coverage, workflows).

            6. **Documentation & Developer Experience:**  
            - How well-documented the project appears (`README.md`, `docs/`, `examples/`, etc.).  
            - Indicators of maintainability and developer onboarding.

            7. **Deployment & Infrastructure:**  
            - How the project might be deployed or released (`Dockerfile`, `k8s/`, `.github/workflows/release.yml`, etc.).  
            - Any cloud/infrastructure hints (Terraform, Helm, etc.).

            8. **Maturity & Professionalism:**  
            - Open source readiness (`LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`).  
            - Whether it looks like a hobby project, prototype, or production-grade system.

            9. **Additional Insights:**  
            - Any notable design patterns, conventions, or unusual elements.  
            - Any likely external integrations (APIs, SDKs, AI models, etc.).

            ---
            **Output format:**  
            Respond in structured Markdown with clear section headers.  
            Be detailed, infer logically, and justify conclusions briefly (e.g., “Presence of `Dockerfile` suggests deployment via containers”).  
            If uncertain, express likelihoods (e.g., “Likely uses FastAPI given `main.py` and `routes/` structure”).

            ---

            You will now receive the repository directory structure as input.
            """
            },
            {
                "role": "user",
                "content": f"Here is the repository structure:\n\n{repo_structure}"
            }
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    reply = response.choices[0].message.content
    return reply


def analyze_file_content(file_content):
    """Use Azure OpenAI to analyze the content of a specific file and provide insights."""
    prompt = f"""
    You are an expert software engineer and code reviewer. Carefully analyze the following file content:

    {file_content}

    Please provide a comprehensive analysis including:

    1. **Purpose and Functionality:** Describe the overall purpose of the file, what problem it is solving, and how it fits into a larger project or system.

    2. **Key Components:** Identify important classes, functions, variables, and modules used, and explain their roles.

    3. **Workflow and Logic:** Explain the main logic, data flow, and control structures, highlighting any important algorithms or patterns.

    4. **Dependencies:** List external libraries, frameworks, or modules the file relies on, and their relevance.

    5. **Strengths and Potential Issues:** Point out well-designed aspects, potential bugs, performance considerations, or maintainability concerns.

    6. **Suggestions/Recommendations:** Recommend any improvements, best practices, or optimizations if applicable.

    Ensure your analysis is clear, structured, and formatted properly using Markdown headings, bullet points, and code blocks where appropriate.
    """
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an expert software engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    reply = response.choices[0].message.content
    return reply
    
def summarize_file_content(file_content):
    """Use Azure OpenAI to summarize the content of a specific file."""
    prompt = f"Summarize the following code file content in a concise manner:\n\n{file_content}"
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an expert software summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500,
    )
    reply = response.choices[0].message.content
    return reply