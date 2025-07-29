import os
import sys
import pandas as pd

from markupsafe import Markup
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

from apps.utility.util_file import markdown_to_html

bp = Blueprint('learning', __name__, url_prefix='/learning') 

# @bp.route('/', methods=['GET'])
# def learning_home():
#     learning_header = "Home"
#     return render_template('learning/learning_home.html', 
#                            learning_header = learning_header)
    
@bp.route('/python', methods=['GET'])
def learning_python():
    learning_header = "Python"
    out = markdown_to_html("apps\\learning_md\\", "Learn_Python.md")
    return render_template('learning/learning_home.html', 
                           learning_header = learning_header,
                           first_contents=Markup(out))


@bp.route('/test', methods=['GET'])
def learning_test():
    return render_template('learning/convert_markdown_to_html.html')


MARKDOWN_FOLDER = 'apps/learning_md'

# Custom markdown extension for enhanced code blocks
class CodeBlockExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.deregister('html_block')
        md.postprocessors.deregister('raw_html')
        md.inlinePatterns.deregister('html')
        
def create_sidebar():
    """Generate sidebar HTML from markdown files in the directory"""
    files = []
    for filename in os.listdir(MARKDOWN_FOLDER):
        if filename.endswith('.md'):
            name = filename[:-3].replace('_', ' ').title()
            files.append({
                'filename': filename,
                'display_name': name
            })
    return files

def render_markdown_with_highlight(content):
    """Render markdown with syntax highlighting for code blocks"""
    # First convert markdown to HTML
    html = markdown.markdown(content, 
        extensions=[
        'fenced_code',
        'codehilite',  # Handles indented code blocks
        'tables',
        # CodeBlockExtension()
        ],
        # Add this configuration for codehilite
        extension_configs = {
            'codehilite': {
                'use_pygments': True,
                'css_class': 'highlight'
            }
        }
    )
    
    # Add syntax highlighting to code blocks
    pattern = re.compile(r'<pre><code class="language-(.*?)">(.*?)</code></pre>', re.DOTALL)
    
    def replacer(match):
        language = match.group(1)
        code = match.group(2)
        
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)
            
        formatter = HtmlFormatter(style='friendly', cssclass='highlight')
        highlighted = highlight(code, lexer, formatter)
        
        # Add copy button
        copy_button = f'<button class="copy-btn" onclick="copyCode(this)">Copy</button>'
        return f'<div class="code-container">{copy_button}{highlighted}</div>'
    
    return pattern.sub(replacer, html)

def get_markdown_content(filename):
    """Read and render markdown file content"""
    try:
        with open(os.path.join(MARKDOWN_FOLDER, filename), 'r', encoding='utf-8') as f:
            content = f.read()
        return Markup(render_markdown_with_highlight(content))
    except FileNotFoundError:
        return None

@bp.route('/')
def home():
    sidebar_files = create_sidebar()
    # Default to first file if available
    default_file = sidebar_files[0]['filename'] if sidebar_files else None
    return render_template('learning/learning_home.html', 
                         sidebar_files=sidebar_files,
                         content=None if not default_file else get_markdown_content(default_file),
                         active_file=default_file)

@bp.route('/<filename>')
def show_markdown(filename):
    sidebar_files = create_sidebar()
    content = get_markdown_content(filename)
    return render_template('learning/learning_home.html',
                         sidebar_files=sidebar_files,
                         content=content,
                         active_file=filename)


    
if __name__ == '__main__':
    # out = create_sidebar()
    # print(out)
    
    out = get_markdown_content("Learn_Python.md")
    print(out)