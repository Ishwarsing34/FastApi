from pydantic import BaseModel


class CreateProduct(BaseModel):
    name:str
    price:int = 0
    category:str
    stock:int = 0



class UpdateProduct(BaseModel):
        name:str = None
        price:int = None
        category:str = None
        stock:int = None