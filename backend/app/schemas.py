# backend/app/schemas.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    status: str = "ok"
    ingested_chunks: List[str] = Field(default_factory=list)
    detail: Optional[str] = None


class RetrievalTraceItem(BaseModel):
    id: str
    score: Optional[float] = None
    payload: Optional[Dict[str, Any]] = None


class Variant(BaseModel):
    id: str
    copy: str
    ctas: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    estimated_length_tokens: Optional[int] = None
    confidence: Optional[float] = None
    formatting: Optional[Dict[str, Any]] = None


class GenerateRequest(BaseModel):
    brand_id: str
    channel: str
    persona: Optional[str] = None
    objective: Optional[str] = "awareness"
    seed_text: Optional[str] = None
    max_variants: int = 3

    class Config:
        schema_extra = {
            "example": {
                "brand_id": "brand_x",
                "channel": "facebook",
                "persona": "young_professional",
                "objective": "awareness",
                "seed_text": "camera battery",
                "max_variants": 3,
            }
        }


class GenerateResponse(BaseModel):
    variants: List[Variant] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    warnings: List[str] = Field(default_factory=list)
    retrieval_trace: List[RetrievalTraceItem] = Field(default_factory=list)
    request_id: Optional[str] = None
    latency_ms: Optional[int] = None
