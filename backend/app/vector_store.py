from qdrant_client import QdrantClient
from qdrant_client.http import models as qm
from app.embeddings import get_embedder
import uuid


class VectorStore:
COLLECTION = 'linda_chunks'


def __init__(self, url=None):
url = url or 'http://localhost:6333'
self.client = QdrantClient(url=url)
self.embedder = get_embedder()
self._ensure_collection()


def _ensure_collection(self):
try:
self.client.get_collection(self.COLLECTION)
except Exception:
self.client.recreate_collection(
collection_name=self.COLLECTION,
vectors_config=qm.VectorParams(size=384, distance=qm.Distance.COSINE),
)


def upsert_chunk(self, text, metadata: dict):
emb = self.embedder.encode(text)
point = qm.PointStruct(id=str(uuid.uuid4()), vector=emb.tolist(), payload={**metadata, 'text': text})
self.client.upsert(collection_name=self.COLLECTION, points=[point])
return point.id


def search(self, query, top_k=6, filter_payload: dict | None = None):
emb = self.embedder.encode(query)
filter_obj = None
if filter_payload:
filter_obj = qm.Filter(must=[qm.FieldCondition(qm.FieldCondition.key(k), qm.MatchValue(value=v)) for k, v in filter_payload.items()])
res = self.client.search(self.COLLECTION, query_vector=emb.tolist(), limit=top_k, query_filter=filter_obj)
return res
