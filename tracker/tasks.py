# tracker/tasks.py
from celery import shared_task
import requests
from bs4 import BeautifulSoup

@shared_task
def scrape_product():
    url = "لینک محصول شما"  # می‌توانید این را از مدل‌هایتان بگیرید
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_name = soup.find('h1').text
    price = soup.find('span', class_='price').text

    # ذخیره اطلاعات در مدل (اگر مدل دارید)
    from .models import Product
    Product.objects.create(name=product_name, price=price)

    return f"نام محصول: {product_name}, قیمت: {price}"
