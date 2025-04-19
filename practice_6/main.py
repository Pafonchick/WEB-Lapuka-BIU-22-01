import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float

class ProductsResponse(BaseModel):
    products: list[Product]

products = [
    Product(id=1, name="Колбаса", price=300.0),
    Product(id=2, name="Хлеб", price=50.0),
    Product(id=3, name="Гвозди", price=100.50),
]

@app.get("/products", response_model=ProductsResponse)
async def get_products() -> ProductsResponse:
    return ProductsResponse(products=products)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=50052, reload=True)