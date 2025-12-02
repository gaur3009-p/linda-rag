from app.vector_store import VectorStore
import os


VECTOR = VectorStore()

def chunk_text(text, chunk_size=200, overlap=40):
  tokens = text.split()
  out = []
  i = 0
  while i < len(tokens):
  chunk = ' '.join(tokens[i:i+chunk_size])
  out.append(chunk)
  i += chunk_size - overlap
  return out




def ingest_file(file_path: str, brand_id: str, vector_store: VectorStore = VECTOR):
  # very basic: reads a .txt file. Extend to pdf/docx/html with parsers.
  assert os.path.exists(file_path), 'file not found'
  text = open(file_path, 'r', encoding='utf-8').read()
  chunks = chunk_text(text)
  ids = []
  for c in chunks:
  meta = {'brand_id': brand_id, 'source': file_path}
  pid = vector_store.upsert_chunk(c, meta)
  ids.append(pid)
  return ids
