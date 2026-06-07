from pydantic import BaseModel
class CreateProduct(BaseModel):
    name: str
    price: int
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    quantity: int