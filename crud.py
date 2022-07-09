"""
    where we handel the products crud
"""
from sqlalchemy.orm import Session
import models, schemas


# get a product by id
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


# get products by user url
def get_products_by_url(db: Session, url: str):
    return db.query(models.Product).filter(models.Product.url == url).all()


#get all products
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return [product.to_dict for product in db.query(models.Product).offset(skip).limit(limit).all()]

# create a product
def create_product(db: Session , product):
    db_product = models.Product(
        **product,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    print(f"created product {db_product.id}")
    return db_product.to_dict
