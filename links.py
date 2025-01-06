import requests
from urllib.parse import urlparse, parse_qs, urlencode
import argparse

def verificar_redireccion(archivo, url_redirigir):
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
                query_params['redirect'] = [url_redirigir]
                
                # Reconstruir la URL con los parámetros modificados
                new_query = urlencode(query_params, doseq=True)
                new_url = parsed_url._replace(query=new_query).geturl()

                # Realizamos una solicitud HTTP a la nueva URL
                try:
                    respuesta = requests.get(new_url, allow_redirects=True)

                    # Verificamos si la página redirige correctamente a la URL proporcionada
                    if url_redirigir in respuesta.url:
                        print(f'URL original: {enlace}')
                        print(f'URL que redirige a {url_redirigir}: {new_url}\n')
                except requests.exceptions.RequestException as e:
                    # Si hay un error en la solicitud (como un enlace roto), lo manejamos aquí
                    print(f'Error al intentar acceder a la URL modificada: {new_url}, error: {e}\n')

if __name__ == '__main__':
    # Crear un parser para los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Verificar redirección de enlaces.')
    
    # Agregar los argumentos -u (URL) y -f (archivo de enlaces)
    parser.add_argument('-u', '--url', type=str, required=True, help='URL específica para el parámetro "redirect"')
    parser.add_argument('-f', '--archivo', type=str, required=True, help='Archivo con los enlaces a verificar')

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # Llamar a la función pasando los parámetros
    verificar_redireccion(args.archivo, args.url)