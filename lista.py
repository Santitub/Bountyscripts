import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL de la página que queremos analizar
url = 'http://172.17.0.2:8080/'

# Realizar la solicitud GET para obtener el contenido de la página
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todas las etiquetas <a> con un atributo href
    links = soup.find_all('a', href=True)

    # Abrir el archivo 'enlaces.txt' en modo escritura
    with open('enlaces.txt', 'w') as file:
        # Iterar sobre los enlaces encontrados y escribirlos en el archivo
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)  # Combina la URL base con la relativa
            file.write(full_url + '\n')  # Escribir la URL en el archivo

    print("Las URLs se han guardado en 'enlaces.txt'.")
else:
    print(f"Error al acceder a la página: {response.status_code}")
