from typing import List, Optional
from pydantic import BaseModel


class QAPair(BaseModel):
    question: str
    answer: str


class Recommendation(BaseModel):
    title: str
    slug: str


class Frontmatter(BaseModel):
    slug: str
    title: str
    description: str
    date: str
    readingTime: int
    tags: List[str]
    qaSection: Optional[QAPair] = None
    recommendations: Optional[Recommendation] = None
