from pydantic import BaseModel

class Product():
    """
        product class that have the following attributes:
        name : str
        price : int
        url : str
        cpu : str
        ram : str
        gpu : str
        description : str
    """
    name : str
    price : int
    url : str
    cpu : str
    ram : str
    gpu : str
    disk : str
    description : str
    
    class Config:
        orm_mode = True