from fastapi import APIRouter, HTTPException
from src.utils.utils import get_all_products, create_product
from src.dtos.productSchema import CreateProduct, UpdateProduct

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