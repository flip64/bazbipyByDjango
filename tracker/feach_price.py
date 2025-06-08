import requests
from bs4 import BeautifulSoup

def fetch_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"خطا در دریافت صفحه: {e}")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # استخراج نام محصول
    name_tag = soup.find("h1", class_="product_title")
    product_name = name_tag.text.strip() if name_tag else None

    # جستجوی چندگانه برای کلاس‌های ممکن قیمت
    price_tag = soup.find("span", class_="woocommerce-Price-amount amount")
    if not price_tag:
        price_tag = soup.find("span", class_="woocommerce-Price-amount")

    product_price = price_tag.text.strip() if price_tag else None

    if not product_name and not product_price:
        print("نام و قیمت محصول یافت نشد.")
    elif not product_name:
        print("نام محصول یافت نشد.")
    elif not product_price:
        print("قیمت محصول یافت نشد.")

    return product_name, product_price
