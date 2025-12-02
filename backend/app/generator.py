from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.retriever import Retriever
import json


# Using Flan-T5 base model as an instruction-following example
TOKENIZER = AutoTokenizer.from_pretrained('google/flan-t5-large')
MODEL = AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-large')


class GenerateRequest(BaseModel):
  brand_id: str
  channel: str
  persona: str | None = None
  objective: str | None = 'awareness'
  seed_text: str | None = None
  max_variants: int = 3
  
  
  class Generator:
    def __init__(self, retriever: Retriever):
      self.retriever = retriever
    
    
    def build_prompt(self, req: GenerateRequest, retrieved_docs: List[dict]):
    # Build instruction with grounding and schema enforcement
      docs_text = '\n\n'.join([f"[SOURCE:{d['id']}] {d['text']}" for d in retrieved_docs])
      instruction = f"You are Linda, an enterprise creative AI for brand. Use the sources to produce {req.max_variants} ad variants for channel {req.channel} with persona {req.persona}.\n"
      instruction += "Return strict JSON with fields: variants (id, copy, ctas[], sources[]), metadata, warnings. Do not hallucinate; if claim not in sources, omit it and add warning."
      prompt = instruction + '\n\nSOURCES:\n' + docs_text + '\n\nOUTPUT:'
      return prompt
    
    
    def generate(self, req: GenerateRequest):
      retrieved = self.retriever.retrieve(req.seed_text or req.objective, brand_id=req.brand_id, top_k=6)
      prompt = self.build_prompt(req, retrieved)
      inputs = TOKENIZER(prompt, return_tensors='pt', truncation=True, max_length=2048)
      outputs = MODEL.generate(**inputs, max_new_tokens=256, do_sample=False, temperature=0.2)
      raw = TOKENIZER.decode(outputs[0], skip_special_tokens=True)
      # Try to parse JSON from model output
      try:
      parsed = json.loads(raw)
      except Exception:
      # fallback wrap
      parsed = {"variants": [{"id": "v1", "copy": raw[:250], "ctas": [], "sources": [d['id'] for d in retrieved]}], "warnings": ["parse_error"]}
      # attach retrieval_trace and latency placeholders
      parsed['retrieval_trace'] = [{'id': d['id'], 'score': d['score']} for d in retrieved]
      return parsed
