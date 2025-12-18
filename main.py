from fastapi import Depends, FastAPI
from model import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session
import logging

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome to telusko track"

products = [
    Product(1, "Phone", "A smartphone", 699.99, 50),
    Product(2, "Laptop", "A powerful laptop", 999.99, 30),
    Product(5, "Pen", "A blue ink pen", 1.99, 100),
    Product(6, "Table", "A wooden table", 199.99, 20),
]

def get_db():
    db=SessionLocal()
    try:
        yield db
    except:
        db.close()

def init_db():
    db = SessionLocal()
    count=db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
init_db()

@app.get("/product")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

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

