from sentence_transformers import SentenceTransformer


class Embedder:
def __init__(self, model_name='all-MiniLM-L6-v2'):
self.model = SentenceTransformer(model_name)


def encode(self, texts):
# accepts list[str] or str
single = False
if isinstance(texts, str):
texts = [texts]
single = True
emb = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
return emb[0] if single else emb


_embedder = None


def get_embedder():
global _embedder
if _embedder is None:
_embedder = Embedder()
return _embedder
