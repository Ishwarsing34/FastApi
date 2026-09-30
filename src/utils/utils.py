import json




file_path ="src/data/products.json"

def get_all_products():
    with open(file_path, 'r') as p:
        return json.load(p)




def create_product(products):
    with open(file_path, 'w') as p:
        json.dump(products, p)