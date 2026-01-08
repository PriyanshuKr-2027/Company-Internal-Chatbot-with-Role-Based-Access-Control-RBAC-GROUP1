from file_loader import load_markdown_files, load_csv_file
from text_cleaner import clean_text
from md_parser import parse_markdown_sections
import json

def process_markdown(md_folder):
    raw_md_files = load_markdown_files(md_folder)
    processed_docs = {}

    for filename, raw_text in raw_md_files.items():
        cleaned_text = clean_text(raw_text)
        sections = parse_markdown_sections(cleaned_text)
        processed_docs[filename] = sections

    return processed_docs


def process_csv(csv_path):
    df = load_csv_file(csv_path)
    df = df.fillna("")
    return df


if __name__ == "__main__":
    MARKDOWN_FOLDER = "../Finance"
    CSV_PATH = "../HR/hr_data.csv"

    md_output = process_markdown(MARKDOWN_FOLDER)
    csv_output = process_csv(CSV_PATH)

    
    with open("cleaned_markdown.json", "w", encoding="utf-8") as f:
        json.dump(md_output, f, indent=2, ensure_ascii=False)

    csv_output.to_csv("cleaned_hr.csv", index=False)

    print("✅ Cleaning & section extraction completed!")
