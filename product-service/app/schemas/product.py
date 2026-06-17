from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: int = Field(ge=0)
    stock_quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock_quantity: int
