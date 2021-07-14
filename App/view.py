"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp 
assert cf


""" 
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*1000000)

def printMenu():
    print("Bienvenido")
    print("1- Inicializar el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Consultar el TOP de videos con más likes que son tendencia en un determinado país, dada una categoría específica.")
    print("4- Consultar el video que más días ha sido trending para un país específico.")
    print("5- Consultar el video con más días de tendencia de una categoría específica")
    print("6- Consultar el top de videos con mas comentarios segun tag y país")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)
        print('Videos cargados: ' + str(controller.videosSize(catalog)))
        print('Categorias cargadas: ' + str(controller.categoriesSize(catalog)))
    
    elif int(inputs[0]) == 3:
        categoria = int(input("ingrese el id de la categoria: "))
        pais = input("ingrese el pais del video: ")
        n = int(input("Número de videos que desea listar: "))
       
        mejores_videos = controller.getBestVideos(catalog, n, categoria, pais)
               
        if mejores_videos == None:
            print("No se encuentra un video con las  características solicitadas")
        else:
            if lt.size(mejores_videos) < n:
                print("El top solicitado es mayor a la cantidad total de videos encontrados. Sin embargo... ")
           
            print("Los videos con más likes en el país", pais, "y en la categoría", categoria, "son: ")
            indice = 1
            for video in lt.iterator(mejores_videos):

                print(str(indice), "-- Trending date: ", video["trending_date"])
                print("Title:", video['title'])
                print("Channel title:", video['channel_title'])              
                print("Publish time:", video['publish_time'])
                print("Views:", video['views'])
                print("Likes:", video['likes'])
                print("Dislikes:", video['dislikes'])

                indice += 1

    elif int(inputs[0]) == 4:
        pais = input("Ingrese el país sobre el cual desea hacer la consulta: ")
        
        bestVideoTuple = controller.getMostTrendingVideoByCountry(catalog, pais)
        bestVideo = bestVideoTuple[0]
        numeroDias = bestVideoTuple[1]

        print("El video con más días en tendencia en", pais, "es: ")
        print("title:  ", bestVideo['title'])
        print("channel title:  ", bestVideo['channel_title'])
        print("country: ", bestVideo['country'])
        print("ratio likes/dislikes", str(float(round(int(bestVideo['likes'])/max(1,int(video['dislikes'])),2))))
        print("Número de días: ", numeroDias )

    elif int(inputs[0]) == 5:

        category = int(input("ingrese la categoria sobre la cual desea hacer la colsulta: " ))

        bestVideoTuple = controller.getMostTrendingVideoByCategory(catalog, category)
        bestVideo = bestVideoTuple[0]
        numeroDias = bestVideoTuple[1]

        print("El video con más días en tendencia en la categoría", category, "es: ")
        print("title:  ", bestVideo['title'])
        print("channel title:  ", bestVideo['channel_title'])
        print("country: ", bestVideo['country'])
        print("ratio likes/dislikes", str(float(round(int(bestVideo['likes'])/int(bestVideo['dislikes']),2))))
        print("Número de días: ", numeroDias )

    elif int(inputs[0]) == 6:

        country = input("Ingrese el país sobre el cual desea consultar: ")
        tag = input("Ingrese el tag: ")
        n = int(input("Número de videos que desea listar: "))
       
        masComentados = controller.getvideoswithmostcomments(catalog, n, country, tag)
               
        if masComentados == None:
            print("No se encuentran videos con las  características solicitadas")
        else:
            if lt.size(masComentados) < n:
                print("El top solicitado es mayor a la cantidad total de videos encontrados. Sin embargo... ")
           
            print("Los videos con más comentarios en el país", country, "y con el tag", tag, "son: ")
            indice = 1
            for video in lt.iterator(masComentados):
                print("----- top", indice, "-----")
                print("Title:", video['title'])
                print("Channel title:", video['channel_title'])              
                print("Publish time:", video['publish_time'])
                print("Views:", video['views'])
                print("Likes:", video['likes'])
                print("Dislikes:", video['dislikes'])
                print("Comment count:", video['comment_count'])
                print("Tags:", video['tags'])

                indice += 1

        

    else:
        sys.exit(0)
sys.exit(0)

 