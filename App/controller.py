"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

from DISClib.DataStructures.rbt import contains
import config as cf
import model
import csv
 

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog 

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadVideos(catalog)

def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    videosFile = cf.data_dir + 'Samples/videos-large.csv'
    input_file = csv.DictReader(open(videosFile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getMostTrendingVideoByCategory (catalog, category_id):

    filteredVideos = model.filterByCategory(catalog, category_id)
    filteredVideos = model.filterByRatioLikesDislikes(filteredVideos, 20)


    return model.getMostTrendingVideo(filteredVideos)

def getMostTrendingVideoByCountry(catalog, pais):
    filteredVideos = model.filterByCountry(catalog, pais)
    filteredVideos = model.filterByRatioLikesDislikes(filteredVideos, 10)


    return model.getMostTrendingVideo(filteredVideos)

def getVideosByCategoryAndCountry (catalog, categoria, pais):
    result = model.getVideosByCategoryAndCountry (catalog, categoria, pais)
    return result


def videosSize(cont):
    """
    Numero de libros cargados al catalogo
    """ 
    return model.videosSize(cont)

def getvideoswithmostcomments(catalog, number, country, tag):
    filteredVideos = model.filterByCountry(catalog, country)
    filteredVideos = model.filterByTag(filteredVideos, tag)

    return model.getMostCommentedVideos(filteredVideos, number)

def getBestVideos(catalog, number, category_id, country):
    
    top = model.getBestVideos(catalog, number, category_id, country)

    return top


def categoriesSize(cont):
    """ 
    Numero de autores cargados al catalogo
    """
    return model.categoriesSize(cont)
