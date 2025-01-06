import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

# Configurar el análisis de argumentos
parser = argparse.ArgumentParser(description='Extraer enlaces de una página web.')
parser.add_argument('-u', '--url', required=True, help='La URL de la página que queremos analizar')
parser.add_argument('-f', '--file', required=True, help='El nombre del archivo donde se guardarán los enlaces')

args = parser.parse_args()

# URL proporcionada como argumento
url = args.url
# Nombre del archivo de salida proporcionado como argumento
output_file = args.file

# Realizar la solicitud GET para obtener el contenido de la página
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todas las etiquetas <a> con un atributo href
    links = soup.find_all('a', href=True)

    # Abrir el archivo de salida en modo escritura
    with open(output_file, 'w') as file:
        # Iterar sobre los enlaces encontrados y escribirlos en el archivo
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)  # Combina la URL base con la relativa
            file.write(full_url + '\n')  # Escribir la URL en el archivo

    print(f"Las URLs se han guardado en '{output_file}'.")
else:
    print(f"Error al acceder a la página: {response.status_code}")
