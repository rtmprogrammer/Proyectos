import os
import sys
import csv
import PyPDF2

def main():
    args = sys.argv[1:]
    pdf_folder=""
    if len(args) == 2 and args[0] == '-pdfs':
        pdf_folder=args[1]
    # Archivo CSV donde exportaremos los resultados    
    csv_file = pdf_folder+"/resultados.csv"

    # Abrimos el archivo CSV y escribimos los encabezados
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["nombre_archivo", "cantidad_paginas", "cantidad_final"])
        # Recorremos cada archivo en la carpeta
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                # Abrimos el archivo PDF
                with open(os.path.join(pdf_folder, filename), "rb") as pdf_file:
                    # Creamos un objeto PdfFileReader para leer el archivo PDF
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    # Obtenemos la cantidad de páginas del archivo
                    num_pages = len(pdf_reader.pages)
                    # Buscamos la cantidad de veces que aparece la palabra "FINAL"
                    count_final = 0
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        count_final += text.count("FINAL")

                    # Escribimos los resultados en el archivo CSV
                    writer.writerow([filename, num_pages, count_final])
    print("¡Los resultados se han exportado correctamente en el archivo CSV!")

# Python boilerplate.
if __name__ == '__main__':
    main()

