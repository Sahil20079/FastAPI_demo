from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

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

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_products_with_id(id: int, db:Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id)
    if db_product:
        return db_product
    return "product not found"
    
@app.post("/products")
def add_product(product: Product, db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db:Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated"
    else:    
        return "product not found"

@app.delete("/products/{id}")
def delete_product(id: int, db:Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "product not found"