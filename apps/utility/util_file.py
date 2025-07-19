import os
import sys
import re

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
 
if __name__ == "__main__":
    out = fileobj_to_string("apps\schema.sql", clear_whitespaces=True)
    print(f"{out=}")