import re

def parse_markdown_sections(md_text):
    """
    Extract headings and their content
    """
    sections = []
    current_section = {
        "title": "ROOT",
        "level": 0,
        "content": []
    }

    for line in md_text.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)

        if heading_match:
            
            sections.append({
                "title": current_section["title"],
                "level": current_section["level"],
                "content": "\n".join(current_section["content"]).strip()
            })

            hashes, title = heading_match.groups()
            current_section = {
                "title": title.strip(),
                "level": len(hashes),
                "content": []
            }
        else:
            current_section["content"].append(line)

    
    sections.append({
        "title": current_section["title"],
        "level": current_section["level"],
        "content": "\n".join(current_section["content"]).strip()
    })

    return sections
