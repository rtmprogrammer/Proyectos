import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile
#urllib2, sys, 
"""
https://www.set.gov.py/documents/20123/465625/ruc0.zip/1ee8368a-ce58-acfa-88f3-4b699bd49f7c?t=1688495339348

------------------------------------------------------------------------------------------------------------------
https://www.set.gov.py/documents/20123/465625/documents/20123/465625/ruc0.zip/1ee8368a-ce58-acfa-88f3-4b699bd49f7c?t=1688495339348


"""

# URL de la página web que deseas rascar
url = "https://www.set.gov.py/web/portal-institucional/listado-de-ruc-con-sus-equivalencias"

# Ruta de destino donde se guardarán los archivos descargados
ruta_destino = "C:/Users/ruthm/Documents/requests"
ruta_descomprimir = "C:/Users/ruthm/Documents/descomprimir"

# Función para encontrar enlaces de archivos .zip
def encontrar_enlaces_zip(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        enlaces_zip = []
        for enlace in soup.find_all("a", href=True):
            # Filtrar enlaces que apunten a archivos .zip
            if re.search(r"\.zip", enlace["href"], re.IGNORECASE):
                enlaces_zip.append(enlace["href"])
        return enlaces_zip
    else:
        print("Error al acceder a la página web.")
        return []

def descargar_archivo(url_archivo, nombre_archivo): 
    response = requests.get(url_archivo) 
    if response.status_code == 200: 
        with open(os.path.join(ruta_destino, nombre_archivo), "wb") as f: f.write(response.content)
        print('\n') 
        print(f"El {nombre_archivo} descargado exitosamente.")
        print ("----------------Contenido del "+nombre_archivo+"------------------") 

        #############################Descomprimir Archivos ZIP####################################
        archivos_zip = zipfile.ZipFile( ruta_destino +"/"+nombre_archivo,'r')
        for name in archivos_zip.namelist():
            archivos_zip.extract(name,ruta_descomprimir)
            print(name)
        archivos_zip.close()   
        
    else: 
        print(f"Error al descargar el archivo {nombre_archivo}.")


# Encontrar enlaces de archivos .zip en la página web especificada
enlaces_zip_encontrados = encontrar_enlaces_zip(url)

 
nombre_doc = 'Archivo'
cont = 0
# Imprimir los enlaces encontrados
if enlaces_zip_encontrados:
    for enlace in enlaces_zip_encontrados:
        if cont < len(enlaces_zip_encontrados) :
            nombre_archivo= nombre_doc+'_'+str(cont)+'.zip'
            enlace_concat =  "https://www.set.gov.py"+enlace
            descargar_archivo(enlace_concat,nombre_archivo)
            cont = cont+1
        else:
            print('ERROR AL DESCARGAR')
    print('=================== Operacion Finalizada ===================')
else:
    print("No se encontraron enlaces de archivos .zip.")