import requests
import lxml.html as html
# Lo usaremos para crear una carpeta
import os
# Lo usaremos para manipular fechas.
import datetime

# Creamos constantes

HOME_URL = 'https://www.larepublica.co/'

#Recuerda que tu Xpath puede variar.
XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_LINK_TO_TITLE = '//div[@class="mb-auto"]/h2/a/text()'
XPATH_LINK_TO_SUMMARY = '//div[@class="wrap-post col-9"]/div/div[@class="lead"]/p/text()'
XPATH_LINK_TO_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:

            # Traigo el docuemnto html de la noticia.
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)


            #Quiero traer el título, el cuerpo y el resumen, hago una validación
            # try -except, estoy haciendolo para los índices de la lista.
            # Pueden haber noticias con nodos faltantes por lo que arrojará un error
            try:
                #Traemos el primer elemento de la lista.
                title = parsed.xpath(XPATH_LINK_TO_TITLE)[0]

                # No es deseable tener comillas en los títulos porque presentan un error en OS.
                # Para solucionar esto, hacemos uso de que title es un str y del metodo replace()                title = title

                title = title.replace('\"','')

                summary = parsed.xpath(XPATH_LINK_TO_SUMMARY)[0]
                body = parsed.xpath(XPATH_LINK_TO_BODY)
            except IndexError:
                return

            # Guardamos en  un archivo

            # with es un manejador contextual. Si algo sucede y el script se cierra, mantiene las cosas
            # de manera segura y así no se corrompe el archivo.

            with open(f'{today}/{title}.txt','w', encoding ='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)



# Creamos las funcioens para ejecutar el script.

def parse_home():
    # Creamos un bloque try para manejar los errores. Y manejar los Status Code.
    try:
        response = requests.get(HOME_URL)
        # Aqui va la lógica para traer los links.
        if response.status_code == 200:
            # .content trae  el HTML que necesita ser traducido con un decode para que python lo entienda
            # en terminos de caracteres, me devuelve un string que no es más que el HTML crudo.
            home = response.content.decode('utf-8')
            # home = response.text
            # print(home)

            # En esta línea uso el parser html para transformar el contentido
            # html a un archivo que sea de utilidad para las expresiones xpath
            parsed = html.fromstring(home)
            print(parsed)

            # En esta línea estoy usando el archivo parseado con la función xpath y le paso por parámetro mi constante
            # la cual almacena la expresión Xpath.

            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # La línea de código me arroja un array vacío. Pero en google si lo enseña.

            print(len(links_to_notices))  # Depende de tu Xpath y la página web.
            print(type(links_to_notices)) # Tipo lista
            print(links_to_notices)

            # Traigo una fecha con la función fecha. Y Today, la fecha del dái de hoy. La variable today
            # se almacena un objeto de tipo fecha, pero nos interesa más tener una cadena de caracteres que contenga la fecha
            # en determinado formato que será guardado en la carpeta y con la función strftime logramos esto

            today = datetime.date.today().strftime('%d-%m-%Y')

            # Este condicional sirve para decirle que si no existe una carpeta con la fehca del día de hoy
            # me cree una carpeta.
            if not os.path.isdir(today):
                os.mkdir(today)

            # Creo la función para recorrer la lista de links y ejecuto en cada ciclo la función parse_notice()
            for link in links_to_notices:
                parse_notice(link,today)



        else:
            #Elevamos el error para ser capturado en el try-except, too lo que sea un error.
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()