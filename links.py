import requests
from urllib.parse import urlparse, parse_qs, urlencode

def verificar_redireccion(archivo):
    # Abrimos el archivo que contiene los enlaces
    with open(archivo, 'r') as f:
        enlaces = f.readlines()

    # Iteramos sobre la lista de enlaces
    for enlace in enlaces:
        enlace = enlace.strip()  # Eliminar espacios y saltos de línea

        # Verificamos si la URL tiene formato correcto (comienza con http:// o https://)
        if enlace.startswith('http://') or enlace.startswith('https://'):
            # Modificamos el parámetro 'redirect' en la URL
            parsed_url = urlparse(enlace)
            query_params = parse_qs(parsed_url.query)
            
            # Si el parámetro 'redirect' está presente, lo modificamos
            if 'redirect' in query_params:
                # Modificar la URL del redireccionamiento
                query_params['redirect'] = ['https://dockerlabs.es']
                
                # Reconstruir la URL con los parámetros modificados
                new_query = urlencode(query_params, doseq=True)
                new_url = parsed_url._replace(query=new_query).geturl()

                try:
                    # Realizamos una solicitud HTTP a la nueva URL
                    respuesta = requests.get(new_url, allow_redirects=True)

                    # Verificamos si la página redirige correctamente (que no sea error.php)
                    if 'error.php' not in respuesta.url:
                        print(f'El enlace que redirige correctamente es: {enlace}')
                except requests.exceptions.RequestException as e:
                    # Si hay un error en la solicitud (como un enlace roto), lo manejamos aquí
                    print(f'Error al intentar acceder a la URL: {new_url}, error: {e}')

# Llamar a la función pasando el archivo de texto como parámetro
archivo = 'enlaces.txt'  # Cambia el nombre del archivo según sea necesario
verificar_redireccion(archivo)