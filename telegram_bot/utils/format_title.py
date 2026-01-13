

def format_title(title: str) -> str:
    return title[1:] if title.startswith('/') else title
