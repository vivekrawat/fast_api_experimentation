from pydantic import BaseModel

class Item(BaseModel):
  name: str
  price: float
  description: str|None = None
  tax: float|None = None

  class Config:
    extra="forbid"
  