import time
import json
# import playwright
from playwright.sync_api import sync_playwright
# import beautifulsoup4
from bs4 import BeautifulSoup


def save_list_to_json(list_to_save : list, file_name : str = 'products.json'):
    with open(file_name, 'w') as f:
        json.dump(list_to_save, f , indent=4)

def load_json_data() -> list:
    with open('products.json') as f:
        return json.load(f)


def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def scroll_to_bottom(page):
    page.evaluate('window.scrollTo(0, document.body.scrollHeight - 1000)')


def get_products_links_by_page(page ):
    # get the element with js-product-list as id 
    products_element = page.query_selector('#js-product-list')
    # get all the divs of the products
    products_links_elem = [div.query_selector('a') for div in products_element.query_selector_all('div.item-product')]
    print(f" found {len(products_links_elem)} products")
    
    return [link.get_property('href') for link in products_links_elem]


def get_products_links_of_all_pages(page , max_pages : int = 11) -> list:
    links = []
    for i in range(1, max_pages):
        print(f'page {i}')
        #go to page url
        page.goto(f'https://www.tunisianet.com.tn/681-pc-portable-gamer?page={i}')
        # scroll down the page
        scroll_to_bottom(page)
        links.append(get_products_links_by_page(page))
    
    return links        


def get_product_info(page , url : str) -> dict:
    url = str(url).replace('\n', '')
    page.goto(url)
    time.sleep(2)
    #get the product title
    infos = page.query_selector('h1.h1').text_content().split('/')
    # get the price
    price_str = page.query_selector('div.current-price').query_selector('span').text_content()
    # get only the numbers in the price str
    price = int(''.join(filter(str.isdigit, price_str)))

    data = {
        "mark": str(infos[0]) ,
        "cpu": str(infos[1]) if len(infos) > 1 else "Null",
        "ram" : str(infos[2]) if len(infos) > 2 else "Null",
        "gpu" : str(infos[3]) if len(infos) > 3 else "Null",
        "disc" : str(infos[4]) if len(infos) > 4 else "Null",
        "price" : str(price) if price else "Null",
        "url" : str(url)
    }
    print(data) 
    print("i m here 1")
    #load json data and append the new product
    json_data = load_json_data()
    print("i m here 2")
    json_data.append(data)
    print("i m here 3")
    # save the data to a json file
    save_list_to_json(json_data)
    print("i m here 4")

def get_products_info(page , urls : list) -> list:
    return [get_product_info(page , url) for url in urls]


def save_links(links : list , file_name : str = 'links.txt'):
    with open(file_name, 'w') as f:
        for link in links:
            f.write(link + '\n')


def load_list(file_name : str = 'links.txt') -> list:
    with open(file_name) as f:
        return f.read().splitlines()

def main():
    # Create a new browser instance
    with sync_playwright() as p:
        # Create a new page
        browser = p.chromium.launch(headless=True)

        page = browser.new_page() # Create a new page # Go to a URL   
        # get the products links list
        # try loading the links from the links.txt file else run the get_products_links_of_all_pages function
        links = load_list() 
        if len(links) == 0:
            links = get_products_links_of_all_pages(page)
            links = flatten_list(links)
            links = [str(link) for link in links]
            # save links to links.txt
            save_links(links)
        
        # get the data from all the products
        products_info = get_products_info(page , flatten_list(links))
        # save the data to a json file
        
        browser.close() # Close the browser


if __name__=="__main__":
    main()