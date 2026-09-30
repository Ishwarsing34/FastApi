import json
import os

from fastapi_mail import ConnectionConfig


file_path ="src/data/products.json"


def get_all_products():
    with open(file_path, 'r') as p:
        return json.load(p)



def create_product(products):
    with open(file_path, 'w') as p:
        json.dump(products, p)


def get_mail_config():
    required_keys = ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_SERVER", "MAIL_FROM"]
    if not all(os.getenv(key) for key in required_keys):
        return None

    return ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )