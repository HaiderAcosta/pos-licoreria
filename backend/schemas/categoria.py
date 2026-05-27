from pydantic import BaseModel

class CategoriaCreate(BaseModel):
    nombre: str

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True
