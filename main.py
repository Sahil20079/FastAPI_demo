from fastapi import FastAPI
from model import Product
from database import SessionLocal, engine
import database_models

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome to telusko track"

products=[
    Product(1,"phone","iphone",99,10),
    Product(2,"laptop","gaming laptop",999,7)
]

def init_db():
    db = SessionLocal()
    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    
init_db()

@app.get("/product")
def get_all_products():
    db = SessionLocal()
    db.query()
    return products

@app.get("/product/{id}")
def get_products_with_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "product not found"
    
@app.post("/product/")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id==id:
           products[i]=product
           return "product successfully added"
    return "product not found"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[id]==id:
            del products[i]
            return "product deleted"
    return "product not found"

