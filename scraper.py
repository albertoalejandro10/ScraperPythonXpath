# import pandas as pd
import lxml.html as html
import requests
import psycopg2

HOME_URL = 'https://garminstore.cl/wearables/productos/todos.html'
XPATH_LINK_TO_PAGINATION = '//li[@class="item pages-item-next"]/a/@href'
XPATH_TITLE = '//strong/a/text()'
XPATH_SUMMARY = '//div[@class="short_description"]/p/text()'
XPATH_PRICE_AMMOUNT = '//div[@class = "price"]/div[@class != "discount_price_nrm" and @class = "price_ammount"]/text()'
XPATH_PRICE_DISCOUNT = '//div[@class="price"]/div[@class!="discount_price_nrm" and @class!="price_ammount"]/div/text()'


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_titles = parsed.xpath(XPATH_TITLE)

            array_titles = []
            for item in links_to_titles:
                iterator = item.strip()

                array_titles.append(iterator)

            links_to_summary = parsed.xpath(XPATH_SUMMARY)

            # precios sin paginar
            links_to_price = parsed.xpath(XPATH_PRICE_AMMOUNT)
            links_to_price_discount = parsed.xpath(XPATH_PRICE_DISCOUNT)
            array_prices_without_pagination = links_to_price + links_to_price_discount

            # enlace para la siguiente pagina de la tienda
            link_to_pagination = parsed.xpath(XPATH_LINK_TO_PAGINATION)
            response_pagination = requests.get(link_to_pagination[0])
            if response_pagination.status_code == 200:
                home_pagination = response_pagination.content.decode('utf-8')
                parsed_pagination = html.fromstring(home_pagination)

                titles_pagination = parsed_pagination.xpath(
                    XPATH_TITLE)

                array_titles_pagination = []
                for item in titles_pagination:
                    iterator = item.strip()
                    array_titles_pagination.append(iterator)

                links_to_summary_pagination = parsed_pagination.xpath(
                    XPATH_SUMMARY)
                links_to_summary_pagination.pop(5)
                links_to_summary_pagination.pop(7)

                # precios con paginar
                links_to_price_paginate = parsed_pagination.xpath(
                    XPATH_PRICE_AMMOUNT)
                links_to_price_discount_paginate = parsed_pagination.xpath(
                    XPATH_PRICE_DISCOUNT)
                array_prices_with_pagination = links_to_price_paginate + \
                    links_to_price_discount_paginate

            # Suma entre arreglo 1 y arreglo 2 de titulos
            array_total_titles = array_titles + array_titles_pagination

            # Suma entre arreglo 1 y arreglo 2 de Reseñas
            array_total_summary = links_to_summary + links_to_summary_pagination

            # Suma entre arreglos 1 y arreglo 2 de precios
            array_total_prices = array_prices_without_pagination + array_prices_with_pagination


                #DATAFRAME: ESTABLECIA TODOS LOS DATOS EN UN CONJUNTO DE DATOS ORGANIZADOS
            # datos = {'titulos': array_total_titles,
            #          'descripcion': array_total_summary, 'precios': array_total_prices}            
            # df = pd.DataFrame(data=datos)
            #print(df)

            array_prices_numbers = []
            for item in array_total_prices:
                iterator = item.replace('.', '')
                array_prices_numbers.append(iterator)

            dbname = 'products'
            host = 'localhost'
            port = '5432'
            user = 'postgres'
            pwd = '1234'

            conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)

            conectar = conn.cursor()

            conectar.execute("""CREATE TABLE products (
                    titulos         TEXT,
                    descripciones   TEXT,
                    precios         TEXT
            )""")

            try:
                contar = 0
                for e in range(len(array_total_titles)):
                    conectar.execute("""INSERT INTO products(titulos, descripciones, precios) VALUES ( """ + "'" + array_total_titles[contar] + "'" + ',' + "'" + array_total_summary[contar] + "'" + ',' + "'" + array_prices_numbers[contar] + "'" + """ ) """)
                    contar = contar + 1
                    print("Envio de datos, exitoso")
            except:
                print("Error al enviar lo datos al servidor PostgreSQL")

            conn.commit()
            conn.close()

            conectar.close()

        else:
            raise ValueError(f'Error:{response.status_code}')

    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()