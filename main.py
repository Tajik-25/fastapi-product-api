from pydantic import BaseModel,Field,field_validator,model_validator
from fastapi import FastAPI,HTTPException
from typing import Optional
app = FastAPI()
products = []
product_id = 1
class Product(BaseModel):
    name:str
    price:int = Field(gt=0)
    quantity:int = Field(gt=0)
    discount:Optional[int] = Field(default=None,ge=0)
    @field_validator("name")
    def len_name(cls,value,info):
        if len(value) < 3:
            raise ValueError ("name cannot be less then 3 letters")
        return  value
    @field_validator("quantity")
    def check_quantity(cls,value,info):
        if value > 50:
            raise ValueError ("quantity cannot exceed 50")
        return value
    @model_validator(mode="after")
    def check_discount(self):
        if self.discount is not None:
            if self.discount > self.price:
                raise ValueError ("discount cannot exceed price")
        return self
class Update(BaseModel):
    price:Optional[int] = None
    quantity:Optional[int] = None
    discount : Optional[int] = None
@app.post("/products")
def create_product(product:Product):
    global product_id
    total = product.price * product.quantity
    if product.discount:
        final_price = total - product.discount
    else:
        final_price = total
    product_data = product.dict()
    product_data["id"] = product_id
    product_data["total"] = total
    product_data["final_price"] = final_price
    products.append(product_data)
    return product_data
@app.get("/products")
def all_products():
    return products
@app.put("/products/{product_id}")
def update_product(product_id:int,update:Update):
    for product in products:
        if product["id"] == product_id:
            if update.price is not None:
                product["price"] = update.price
            if update.quantity is not None:
                product["quantity"] = update.quantity
            if update.discount is not None:
                product["discount"] = update.discount
        total = product["price"] * product["quantity"]
        product["total"] = total
        if product.get("discount") is not None:
            final_price = total - product["discount"]
        else:
            final_price = total
        product["final_price"] = final_price 
        
        return product
    raise HTTPException(status_code=404,detail="product not found")
@app.delete("/products/{product_id}")
def delete_product(product_id:int):
    for index,product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)
            return {"success":"product deleted"}
    raise HTTPException(status_code=404,detail="product not found")

