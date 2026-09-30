from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema

from src.utils.utils import get_all_products, create_product, get_mail_config
from src.dtos.productSchema import CreateProduct, UpdateProduct, OrderSchema

productRoutes = APIRouter()

@productRoutes.get("/")
def getAllProducts(product_id: int = None):
    allProducts = get_all_products()
    if not product_id:
        return allProducts
    
    for product in allProducts:
            if product["id"] == product_id:
                return product
    return HTTPException(status_code=400, detail={"error" : "product not found for this id"})
        


#path params
@productRoutes.get("/{id}")
def getOneProduct(id:int):
   
    allProducts = get_all_products()

    for product in allProducts:
        if product["id"] == id:
            return product
    return HTTPException(status_code=400, detail={"error" : "product not found for this id"})
    


@productRoutes.post("/create")
def createTheProducts(product:CreateProduct):
    products = get_all_products()
    product_data = product.model_dump()
    product_data["id"] = max((p["id"] for p in products), default=0) + 1
    products.append(product_data)
    create_product(products)
    return {"message" : "new product created successfully"}



@productRoutes.put("/update/{id}")
def updateProduct(product:UpdateProduct, id:int = None):
     if not id:
          return HTTPException(status_code=400, detail={"error":"product id not found"})

     oneProduct = None
     AllProducts = getAllProducts()

     for index, p in enumerate(AllProducts) :
          if p["id"] == id:
               changes = {}
               
               for k, v, in product.model_dump().items():
                    if v is not None:
                         changes[k] = v

               AllProducts[index] = {"id":id , **p, **changes}
               
               return {"message" : "product updated successfully"}

     return HTTPException(status_code=400, detail={"error":"Product ID not found"})



@productRoutes.delete("/delete/{id}")
def deleteProduct(id: int = None):
    if not id:
        return HTTPException(
            status_code=400,
            detail={"error": "product id not found"}
        )

    AllProducts = getAllProducts()

    for index, p in enumerate(AllProducts):
        if p["id"] == id:
            AllProducts.pop(index)

            return {
                "message": "product deleted successfully"
            }

    return HTTPException(
        status_code=400,
        detail={"error": "Product ID not found"}
    )






@productRoutes.post("/order")
async def PlaceOrder(orderDetails:OrderSchema, background_tasks: BackgroundTasks):
    count = orderDetails.count
    product_id = orderDetails.product_id
    email = orderDetails.email

    if count <= 0:
        raise HTTPException(status_code=400, detail={"error": "order quantity must be greater than 0"})

    if product_id is None:
        raise HTTPException(status_code=400, detail={"error": "product id is required"})

    if not email:
        raise HTTPException(status_code=400, detail={"error": "email is required"})

    allProducts = get_all_products()
    oneProduct = None

    for index, p in enumerate(allProducts):
        if p["id"] == product_id:
            oneProduct = p
            break

    if not oneProduct:
        raise HTTPException(status_code=400, detail={"error": "product id not found"})

    if oneProduct["stock"] < count:
        raise HTTPException(
            status_code=400,
            detail={"error": "insufficient stock for this product"}
        )

    oneProduct["stock"] -= count
    create_product(allProducts)

    mailConfig = get_mail_config()
    if mailConfig is not None:
        message = MessageSchema(
            subject="Order placed successfully",
            recipients=[email],
            body=(
                f"Hello,\n\n"
                f"Your order for {oneProduct['name']} has been placed successfully.\n"
                f"Quantity: {count}\n"
                f"Remaining stock: {oneProduct['stock']}\n"
            ),
            subtype="plain",
        )

        async def send_email_in_background():
            fm = FastMail(mailConfig)
            await fm.send_message(message)

        background_tasks.add_task(send_email_in_background)

    return {
        "message": "Order placed successfully",
        "product_id": product_id,
        "email": email,
        "quantity": count,
        "remaining_stock": oneProduct["stock"]
    }