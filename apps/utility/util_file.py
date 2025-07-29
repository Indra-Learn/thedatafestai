import os
import sys
import re
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.codehilite import CodeHiliteExtension


parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(parentdir)

def fileobj_to_string(file_path: str, encoding=None, clear_whitespaces=True):
    try:
        with open(file=file_path, mode="r", encoding=encoding) as file_obj:
            content = file_obj.read()
    except FileNotFoundError as e: 
        print(f"Error: File not find at {file_path}")
    if clear_whitespaces:
        cleaned_content = content.strip()
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)            
        return cleaned_content
    else:
        return content
    
    
class NoLanguagePreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            new_lines.append(re.sub(r'^```[a-zA-Z0-9_+-]*', '```', line))
        return new_lines

class NoLanguageExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(NoLanguagePreprocessor(), 'no_language', 10)
    
def markdown_to_html(basefile_path, md_file_name):
    if not md_file_name.endswith('.md'):
        md_file_name += '.md'
    full_path = basefile_path +"\\" + md_file_name
    safe_filename = os.path.basename(full_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        # html_content = markdown.markdown(md_content,  extensions=[NoLanguageExtension(), 'fenced_code', 'codehilite'])
        html_content = markdown.markdown(md_content,  extensions=['fenced_code', CodeHiliteExtension(linenums=False, guess_lang=True)])
        # md = markdown.Markdown(extensions=[, 'fenced_code'])
        # html_content = md.convert(md_content)
        template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{safe_filename}</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown.min.css">
                <style>
                    .markdown-body {{
                        box-sizing: border-box;
                        min-width: 200px;
                        max-width: 980px;
                        margin: 0 auto;
                        padding: 5px;
                    }}
                </style>
            </head>
            <body>
                <article class="markdown-body">
                    {html_content}
                </article>
            </body>
            </html>
        """
        return template
    except FileNotFoundError:
        return "Markdown file not found", 404

 
if __name__ == "__main__":
    # out = fileobj_to_string("apps\schema.sql", clear_whitespaces=True)
    # print(f"{out=}")
    
    out = markdown_to_html("apps\\learning_md\\", "Lear_Python.md")
    print(out)