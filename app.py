from flask import Flask, render_template_string
import boto3
import mysql.connector

app = Flask(__name__)

# Konfigurasi S3
S3_BUCKET = 'product-bucket179'
S3_REGION = 'asia-southeast2'

# Konfigurasi Database
db_config = {
    'host': '34.101.223.8',
    'user': 'root',
    'password': 'silviana19',
    'database': 'Ecommerce'
}

html_template = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Produk Kami</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 32px; margin-bottom: 20px; }
        .product { display: inline-block; width: 30%; margin: 20px; text-align: center; }
        img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 10px; }
        .price { font-size: 20px; color: green; margin-top: 10px; }
        .product-name { font-size: 20px; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Produk Kami</h1>
        {% for image_url, name, price in products %}
        <div class="product">
            <img src="{{ image_url }}" alt="Produk">
            <p class="product-name">{{ name }}</p>
            <p class="price">Rp{{ price }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    # Ambil URL gambar dari S3
    image_urls = [
     "https://storage.googleapis.com/product-bucket179/aktuator.png",
     " https://storage.googleapis.com/product-bucket179/Base.png",
     "https://storage.googleapis.com/product-bucket179/gyroscope.png",
     "https://storage.googleapis.com/product-bucket179/gripper.png"
]

    # Koneksi ke database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT nama,  harga FROM produk;")
    #harga = cursor.fetchone()[0]
    product_data = cursor.fetchall()

    cursor.close()
    connection.close()

    products = zip(image_urls, [data[0] for data in product_data], [data[1] for data in product_data])
    #return render_template_string(html_template, products=products)
    return render_template_string(html_template, products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



