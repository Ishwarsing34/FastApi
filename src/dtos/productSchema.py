from pydantic import BaseModel, EmailStr


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



class OrderSchema(BaseModel):
      count:int =  1
      product_id:int = None
      email:EmailStr = None


class UserResponse(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserMessage(BaseModel):
    message: str
    user: UserResponse