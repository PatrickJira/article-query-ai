from markdown import Markdown
from io import StringIO
import re

def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    text = re.sub(r'\\n', '\n', text)
    return __md.convert(text)

def strip_tags(html):
  return re.sub('<[^<]+?>', '', html)

def clean_text(text: str):
    if text:
        lines = text.splitlines()
        text = '\n'.join([line for line in lines if line.strip()])
        text = re.sub(r'[ \t]+', ' ', text).strip()
        return text
    return text

def write_dict_to_file(data, file, indent=0):
    """Recursively write dictionary content to file with proper indentation."""
    for key, value in data.items():
        if isinstance(value, dict):
            file.write(f"{' ' * indent}{key}:\n")
            write_dict_to_file(value, file, indent + 4)
        elif isinstance(value, list):
            file.write(f"{' ' * indent}{key}:\n")
            for item in value:
                if isinstance(item, dict):
                    write_dict_to_file(item, file, indent + 4)
                else:
                    file.write(f"{' ' * (indent + 4)}- {item}\n")
        else:
            file.write(f"{' ' * indent}{key}: {value}\n")

