# Scraper en Python usando XPath

Script desarrollado para extraer el nombre, descripcion y precios de los productos de la pagina https://garminstore.cl/wearables/productos/todos.html y almacenarlos en una base de datos PostgreSQL.

## Instalación

Instalar la carpeta venv/ y luego instalar los paquetes requeridos por consola.

```bash
python3 -m venv venv
```

## Uso

- Crear una base de datos en un servidor PostgreSQL, por ejemplo, pgAdmin 4 y modificar las variables para la conexion a la base de datos dentro del programa.

- Entrar al modo de desarollo venv desde Ubuntu

```
source venv/bin/activate

```

Luego deberas correr el scraper.py

```
python3 scraper.py

```

Si todo salio correctamente, debera aparecer una serie de resultados exitosos y ya debe haber guardado los datos extraidos de Garmin Chile de los productos en PostgreSQL.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
