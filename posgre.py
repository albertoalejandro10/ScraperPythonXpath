import psycopg2

dbname = 'dbtest'
host = 'localhost'
port = '5432'
user = 'postgres'
pwd = '1234'

conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)

conectar = conn.cursor()
conectar.execute("""INSERT INTO products(titulos, descripciones, precios) VALUES ('Casio Reloj', 'Reloj Duradero', '1000')""")

conn.commit()
conn.close()

conectar.close()