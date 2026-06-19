from pydantic import BaseModel
from datetime import datetime
class CreateProduct(BaseModel):
    name: str
    price: int
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    quantity: int
    created_at: datetime