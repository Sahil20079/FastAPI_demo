from pydantic import BaseModel

class Product(BaseModel):
    id : int
    name : str
    description : str
    price : float
    quantity : int
    
    def __init__(self,id: int,name: str,description: str,price: float, quantity: int):
        super().__init__(id=id,name=name,description=description,price=price,quantity=quantity)
