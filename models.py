from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base



class Product(Base):
    """
        product class that have the following attributes:
        name : str
        price : int
        url : str
        cpu : str
        ram : str
        gpu : str
        description : list[str]
    """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True , nullable=True)
    url = Column(String(256), index=True , nullable=True , unique=True)
    cpu = Column(String(256), index=True , nullable=True)
    ram = Column(String(256), index=True , nullable=True)
    gpu = Column(String(256), index=True , nullable=True)
    disk = Column(String(256), index=True , nullable=True)
    price = Column(Integer)
    description = Column(String(256) , index=True , nullable=True)
    
    @property
    def get_descriptions(self):
        # get all the descriptions of this product
        if self.description:
            return self.description.split("\n")
        return []
    
    @property
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "cpu": self.cpu,
            "gpu": self.gpu,
            "ram": self.ram,
            "disk": self.disk,
            "price": self.price,
            "description": self.get_descriptions,
        }
    
    
    def __str__(self):
        return f"{self.name} - {self.price} - {self.url}"
  
    
        

