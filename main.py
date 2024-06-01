import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from pyngrok import ngrok
import threading

app = Flask(__name__)


def parse_product_card(card):
    ids = [
        ['a', 'text-dark h6 font-weight-normal line-clamp-2', 'href', 'product_id=', 11],
        ['a', 'dropdown-item dropdown-item pl-2 pr-2', 'onclick', 'add(', 5, '\');', 0]
    ]
    product_id = None
    # Здесь нужно извлечь 6 свойств товара
    # Пример свойств может включать название, цену, изображение, описание и т.д.
    # В реальном коде замените 'title', 'price', 'image_url', 'description' на реальные классы или идентификаторы

    title = card.find('a', class_='text-dark h6 font-weight-normal line-clamp-2').text.strip()  # замените 'title-class' на реальный класс
    price = card.find('div', class_='h6 mb-1').text.strip()[:-2]  # замените 'price-class' на реальный класс
    image_url = card.find('img', class_='position-absolute t-0 l-0 img-fluid d-block w-auto ft-lazy-img')['src']
    description = card.find('div', class_='product-text d-none font-weight-light text-secondary mb-3').text.strip()  # замените 'description-class' на реальный класс
    # Пример дополнительных свойств
    in_stock = card.find('span', class_="col").text.strip()[-2:] # замените 'property1-class' на реальный класс
    for i in ids:
        try:
            product_id = card.find(i[0], class_=i[1])[i[2]]
            if len(i) == 5:
                product_id = product_id[product_id.index(i[3])+i[4]]
            else:
                product_id = product_id[product_id.index(i[3])+i[4]:product_id.index(i[5])-i[6]]
            break
        except:
            pass

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
    print(product_cards)

    products = []
    for card in product_cards:
        product = parse_product_card(card)
        products.append(product)
    return products


@app.route('/', methods=['POST'])
def parse_endpoint():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        products = parse_site(url)
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    http_tunnel = ngrok.connect("5000", "http").public_url
    print(http_tunnel)
    app.run()


