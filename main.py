from fastapi import FastAPI
from src.routes.productRoute import productRoutes

app = FastAPI(
    title="fastapi crash course",
    description="we are gonna learn and become the good dev in india"
)


@app.get("/")
def Home():
    return {
        "message":"Hello ishwar you are very focused and talented person u got 12+LPA offer by the end of december 2026"
    }


#### CRUD API - Products -- JSON FILE

app.include_router(productRoutes, prefix="/products")







