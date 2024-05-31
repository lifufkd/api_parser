import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from pyngrok import ngrok
import threading

app = Flask(__name__)


def parse_product_card(card):
    # Здесь нужно извлечь 6 свойств товара
    # Пример свойств может включать название, цену, изображение, описание и т.д.
    # В реальном коде замените 'title', 'price', 'image_url', 'description' на реальные классы или идентификаторы

    title = card.find('a', class_='text-dark h6 font-weight-normal line-clamp-2').text.strip()  # замените 'title-class' на реальный класс
    price = card.find('div', class_='h6 mb-1').text.strip()[:-2]  # замените 'price-class' на реальный класс
    image_url = card.find('img', class_='position-absolute t-0 l-0 img-fluid d-block w-auto ft-lazy-img')['src']
    description = card.find('div', class_='product-text d-none font-weight-light text-secondary mb-3').text.strip()  # замените 'description-class' на реальный класс
    # Пример дополнительных свойств
    in_stock = card.find('span', class_="col").text.strip()[-2:] # замените 'property1-class' на реальный класс
    product_id = card.find('a', class_='text-dark h6 font-weight-normal line-clamp-2')['href']
    product_id = product_id[product_id.index('product_id=')+11:]

    return {
        'title': title,
        'price': price,
        'image_url': image_url,
        'description': description,
        'in_stock': in_stock,
        'product_id': product_id
    }


def parse_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти карточки товаров, замените 'product-card-class' на реальный класс карточки товара
    product_cards = soup.find_all('div', class_='col product-item d-flex mb-2')[:3]

    products = []
    for card in product_cards:
        product = parse_product_card(card)
        products.append(product)
    return products


@app.route('/parse', methods=['GET'])
def parse_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        products = parse_site(url)
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    http_tunnel = ngrok.connect("5000", "http")
    print(http_tunnel.public_url)
    app.run()


