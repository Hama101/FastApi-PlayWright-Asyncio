import time
import json
import requests
import asyncio
# import playwright as async_playwright
from playwright.sync_api import sync_playwright
#import playwright as async_playwright
from playwright.async_api import async_playwright
# import beautifulsoup4
from bs4 import BeautifulSoup


# local host url for fastapi server
BASE_URL = "http://localhost:8000"

#Products class
class Product:
    def __init__(self, url : str , page ):
        self.url = url
        self.page = page

    def check_url_in_db(self):
        # a post request to check if the url is in the db to the f"{BASE_URL}/products/url"
        #if null return false
        response = requests.post(f"{BASE_URL}/products/url", json={"url": self.url})
        response_products = response.json()
        if len(response_products) == 0:
            return False
        return True

    async def check_url_in_db_async(self):
        return await asyncio.to_thread(self.check_url_in_db)
    
    async def get_info_async(self):
        #inner function to get the info of the product    
        async def get_product_info(page = self.page , url : str = self.url) -> dict:
            url = str(url).replace('\n', '')
            await page.goto(url)
            #get the product title
            infos = await page.query_selector('h1.h1')
            infos = await infos.text_content()
            infos = infos.split('/')
            # get the price
            price_str =  await page.query_selector('div.current-price')
            price_str = await price_str.query_selector('span')
            price_str = await price_str.text_content()
            # get only the numbers in the price str
            price = int(''.join(filter(str.isdigit, price_str)))
            
            # get the description text
            description =  await page.query_selector('div.product-information')
            description = await description.query_selector('div')
            description = await description.query_selector('p')
            description = await description.text_content()
            
            data = {
                "name": str(infos[0]) ,
                "cpu": str(infos[1]) if len(infos) > 1 else "Null",
                "ram" : str(infos[2]) if len(infos) > 2 else "Null",
                "gpu" : str(infos[3]) if len(infos) > 3 else "Null",
                "disk" : str(infos[4]) if len(infos) > 4 else "Null",
                "price" : str(price) if price else "Null",
                "url" : str(url)
            }
            return data
        #how the schape of the product will be :
        # {name : str , price : int , url : str , cpu : str , ram : str , gpu : str , description : str}
        #return a dictonary with the product infos
        infos = await get_product_info()
        print(f"got data from {self.url}")
        return {
            'url' : self.url,
            **infos
        }
    
    async def save_to_db_async(self):
        if not await self.check_url_in_db_async():
            #save the product to the db
            json_data = await self.get_info_async()
            response = requests.post(f"{BASE_URL}/products", json=json_data)
            response_data = response.json()
            print(f"response from server : {response_data}")
            return response_data
        return {"message": "The product is already in the db"}
    

def load_links():
    with open('links.txt', 'r') as f:
        links = f.readlines()
    return links

async def load_links_async():
    return await asyncio.to_thread(load_links)


async def run(playwright):
    chrome = playwright.chromium
    browser = await chrome.launch()
    #create a page
    page = await browser.new_page()
    #load the links from the links.txt file
    links = await load_links_async()
    #create a list of products
    products = [Product(url, page) for url in links]
   
    # use asyncio.gather to run all the tasks
    # products_info = await asyncio.gather(*[product.get_info_async() for product in products]) 
    for product in products:
        try:
            await product.save_to_db_async() 
        except Exception as e:
            print(e)
            continue
    #close the page
    await page.close()
    #close the browser
    await browser.close()
    #return the products
    return products


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
      

if __name__=="__main__":
    asyncio.run(main())