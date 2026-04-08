from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional
app = FastAPI()
products = []
current_id = 1
class Product(BaseModel):
    name:str
    price: int
    quantity:int
    discount:Optional[int]= None
class Update(BaseModel):
    price:Optional[int]= None
    quantity:Optional[int]= None
    discount:Optional[int]= None
@app.post("/product")
def create_product(product:Product):
    global current_id
    total = product.price * product.quantity
    if not product.discount == None:
        final_price = total - product.discount
    else:
        final_price = total
    product_data = product.dict()
    product_data["id"] = current_id
    product_data["total"] = total
    product_data["final_price"] = final_price
    products.append(product_data)
    current_id += 1
    return product_data
@app.get("/product")
def all_product(min_price:int=0):
    filter = []
    for product in products:
        if product["price"] >= min_price:
            filter.append(product)
    return filter
@app.get("/product/{product_id}")
def get_product(product_id:int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error":"product not found"}
@app.put("/product/{product_id}")
def update_product(product_id : int,update:Update):
    for product in products:
        if product["id"] == product_id:
            if not update.price == None:
                product["price"] = update.price
            if not update.quantity == None:
                product["quantity"] = update.quantity
            if not update.discount == None:
                product["discount"] = update.discount
        total = product["price"] * product["quantity"]
        if update.discount:
            final_price = total - update.discount
        else:
            final_price = total
        product["final_price"] = final_price
        product["total"] = total
        return product
    return {"error":"product not found"}
@app.delete("/product/{product_id}")
def delete_product(product_id:int):
    for i,product in enumerate(products):
        if product["id"] == product_id:
            products.pop(i)
            return {"message":"product deleted"}
    return {"error":"product not found"}



