from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# get all products
@app.get("/products")
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

# get a product by id
@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id=product_id)

#get products by url
@app.post("/products/url")
def get_products_by_url(data: dict, db: Session = Depends(get_db)):
    url = data.get("url")
    print(url)
    return crud.get_products_by_url(db, url=url)

# create a product
@app.post("/products")
def create_product(product : dict , db: Session = Depends(get_db)):
    try :
        return crud.create_product(db, product=product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)