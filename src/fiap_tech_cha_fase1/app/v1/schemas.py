"""
Schemas para a API de Livros
id,titulo,preco,rating,disponibilidade,categoria,imagem_local
"""

from pydantic import BaseModel, Field, constr
from typing import List, Optional, Literal
from datetime import datetime

class LivroBase(BaseModel):
    id: str = Field(..., json_schema_extra={"example": "047dfa57ba0bf638"})
    titulo: str = Field(..., json_schema_extra={"example": "O Senhor dos Anéis"})
    preco: str = Field(..., json_schema_extra={"example": "39.90"})
    rating: str = Field(..., json_schema_extra={"example": "Two"})
    disponibilidade: Literal["In stock", "Out of stock"] = Field(..., json_schema_extra={"example": "In stock"})
    categoria: str = Field(..., json_schema_extra={"example": "Fantasia"})
    imagem_local: Optional[str] = Field(None, json_schema_extra={"example": "/imagens/senhor_dos_aneis.jpg"})