import re

from app.config import CHUNK_OVERLAP, CHUNK_SIZE

def is_heading(line: str):
    line = line.strip()

    if not line:
        return False

    patterns = [
        r"^#{1,6}\s+.+",      # # Introduction
        r"^\d+\.\s+.+",       # 1. Introduction
        r"^\d+\.\d+\s+.+",    # 1.1 Introduction
        r"^[A-Z][A-Z\s]{3,}$", # INTRODUCTION
    ]

    return any(re.match(pattern, line) for pattern in patterns)

def split_into_sections(text):
    sections = []

    current_heading = "Introduction"
    current_lines = []

    for line in text.splitlines():

        if is_heading(line):
            if current_lines:
                sections.append({
                    "heading": current_heading,
                    "text": "\n".join(current_lines).strip()
                })

            current_heading = line.strip()
            current_lines = []

        else:
            current_lines.append(line)

    if current_lines:
        sections.append({
            "heading": current_heading,
            "text": "\n".join(current_lines).strip()
        })

    return sections

def chunk_by_sentence(
    pages,
    file_name,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
):
    if chunk_size <= 0:
        raise ValueError("chunk size must be greater than 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk size")

    chunks = []
    chunk_id = 1
    step = chunk_size - overlap

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        sections = re.split(
            r"(?m)^(?=\d+\.\s+|#{1,6}\s+)",
            text.strip()
        )

        for section in sections:
            section = section.strip()

            if not section:
                continue

            sentences = re.split(
                r"(?<=[.!?])\s+",
                section
            )

            for i in range(0, len(sentences), step):
                chunk = sentences[i:i + chunk_size]

                if not chunk:
                    continue

                chunks.append({
                    "chunk_id": f"{file_name}_p{page_number}_c{chunk_id}",
                    "file_name": file_name,
                    "page_number": page_number,
                    "content": " ".join(chunk)
                })

                chunk_id += 1

    return chunks