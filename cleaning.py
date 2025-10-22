import re
def clean_md_content(md_content):
    """Clean up markdown content by removing excessive newlines and trimming whitespace."""
    # Replace multiple newlines with a single newline
    if re.search(r'^`{3}markdown', md_content, re.MULTILINE):
        cleaned_content = re.sub(r'`{3}markdown\s*\n+', '' , md_content)
    return cleaned_content