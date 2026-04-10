from pydantic import BaseModel,Field,field_validator
from fastapi import FastAPI
from typing import Optional
app = FastAPI()
products = []
class Product(BaseModel):
    name:str
    price:int = Field(gt=0)
    quantity:int = Field(gt=0)
    discount:Optional[int] = Field(default=None,ge=0)
    @field_validator("name")
    def len_check(cls,value,info):
        if len(value) < 3:
            raise ValueError ("name length smaller then 3")
        return value
    @field_validator("quantity")
    def quantity_check(cls,value,info):
        if value > 100:
            raise ValueError("quantity can be greater than 100")
        return value
    @field_validator("discount")
    def check_discount(cls,value,info):
        price = info.data.get("price")
        if value > price:
            raise ValueError ("DISCOUNT cant be greater than price")
        return value
@app.post("/products")
def create_product(product:Product):
    products.append(product.dict())
    return product.dict()
@app.get("/products")
def all_products():
    return products
