from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from db.vector_store import add_embeddings

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def chunk_text(text, chunk_size=500, overlap=100):
    sentences = text.split(". ")

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def embed_chunks(chunks):
    return model.encode(chunks).tolist()


def ingest_document(file_path):
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)

    add_embeddings(embeddings, chunks)

    print(f"Ingested {len(chunks)} chunks")