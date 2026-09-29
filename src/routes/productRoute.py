from fastapi import APIRouter



productRoutes = APIRouter()

@productRoutes.get("/get-all")
def getAllProducts():
    return []



@productRoutes.create("/create")
def createTheProducts():
    return []