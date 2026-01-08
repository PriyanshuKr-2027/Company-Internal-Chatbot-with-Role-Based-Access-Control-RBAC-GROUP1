from pathlib import Path
import pandas as pd

def load_markdown_files(folder_path):
    """
    Load all markdown files from a folder.
    Returns dict {filename: raw_text}
    """
    md_files = {}
    folder = Path(folder_path)

    for file in folder.glob("*.md"):
        md_files[file.name] = file.read_text(encoding="utf-8", errors="ignore")

    return md_files


def load_csv_file(csv_path):
    """
    Load CSV using pandas safely
    """
    return pd.read_csv(csv_path, encoding="utf-8", dtype=str)
