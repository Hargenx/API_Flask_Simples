import logging
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
# Configuração do logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Função para conectar ao banco de dados com logging
def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    logger.info('Connected to database')
    return conn

# Rota para obter um produto específico
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    if product is None:
        logger.error(f'Product with id {product_id} not found')
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(dict(product))

# Implementação de segurança básica (exemplo)
def is_valid_api_key(api_key):
    # Verificação simples de chave API (apenas para demonstração)
    return api_key == 'my_secret_api_key'

# Rota protegida para adicionar um novo produto com autenticação
@app.route('/secure/products', methods=['POST'])
def add_secure_product():
    api_key = request.headers.get('Authorization')
    if not api_key or not is_valid_api_key(api_key):
        logger.warning('Unauthorized access to secure endpoint')
        return jsonify({'error': 'Unauthorized'}), 401

    new_product = request.get_json()
    if 'name' not in new_product or 'price' not in new_product:
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)',
                   (new_product['name'], new_product['price']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added securely'}), 201

if __name__ == '__main__':
    app.run(debug=True)