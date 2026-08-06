import re

# chunk by sentence
def chunk_by_sentence(pages,chunk_size=5,overlap=1):
    if chunk_size <= 0:
        raise ValueError("chunk size must be greater then 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be less then chunk size")

    chunks = []
    step = chunk_size - overlap
    chunk_id = 1

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
        for i in range(0,len(sentences),step):
            chunk = sentences[i : i+chunk_size]
            if chunk:
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "page_number":page_number,
                        "content":" ".join(chunk)
                    }
                )
            chunk_id += 1
            
    return chunks
