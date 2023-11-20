import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Criar tabela de produtos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

# Inserir alguns dados de exemplo
cursor.execute('''
    INSERT INTO products (name, price) VALUES
    ('Product 1', 19.99),
    ('Product 2', 29.99)
''')

# Commit e fechar conexão
conn.commit()
conn.close()
