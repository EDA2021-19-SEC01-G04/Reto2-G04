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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

 
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as se
assert cf
from datetime import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'categories': None,
               'countries': None}

    catalog['videos'] = lt.newList('ARRAY_LIST', compareVideosIds)
    
    """ 
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los videos de la lista
    creada en el paso anterior.
    """
    catalog['videoIds'] = mp.newMap(371291,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapVideoIds)

    """
    Este indice crea un map cuya llave es el identificador del video
    """
    catalog['categories'] = mp.newMap(50,
                                   maptype='CHAINING',
                                   loadfactor = 0.75, comparefunction=compareMapCategoryIds)
    
    catalog['countries'] = mp.newMap(200,
                                   maptype='CHAINING',
                                   loadfactor = 0.75, comparefunction=compareCountriesByName)
    
    return catalog


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    mp.put(catalog["videoIds"], video["video_id"], video)

    addVideoCategory(catalog, video)
    addVideoCountry(catalog, video)

# Funciones para creacion de datos

def addVideoCountry(catalog, video):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    countriesMap = catalog['countries']
    countryName = video["country"]

    existCountry = mp.contains(countriesMap, countryName)
    if existCountry:
        entry = mp.get(countriesMap, countryName)
        country = me.getValue(entry)
    else:
        country = newCountry(countryName)
        mp.put(countriesMap, countryName, country)
    lt.addLast(country['videos'], video)

def addVideoCategory(catalog, video):
    try:
        categories = catalog['categories']
        category_id = video['category_id']
        category_id = int(float(category_id))
        
        existCategory = mp.contains(categories, category_id)
        if existCategory:
            entry = mp.get(categories, category_id)
            categoryEntry = me.getValue(entry)
        else:
            categoryEntry = newCategoryEntry(category_id)
            mp.put(categories, category_id, categoryEntry)
        lt.addLast(categoryEntry['videos'], video)
    except Exception:
        return None

def newCountry(name):
    country = {'name': "",
              "videos": None
              }
    country['name'] = name
    country['videos'] = lt.newList('ARRAY_LIST', compareCountriesByName)
    return country

def newCategoryEntry(category_id):
    entry = {'category': "", "videos": None}
    entry['category'] = category_id
    entry['videos'] = lt.newList('ARRAY_LIST', compareCategories)
    return entry

# Funciones de consulta


def filterByRatioLikesDislikes (listaFiltrada, minratio):

    filteredByRatio = lt.newList()
    for video in lt.iterator(listaFiltrada):
        ratio = int(video['likes'])/max(1,int(video['dislikes']))

        if (ratio > minratio):
            lt.addLast(filteredByRatio, video)
    
    return filteredByRatio

def filterByTag(listaFiltrada, tag):
    filtered = lt.newList()

    for video in lt.iterator(listaFiltrada):
        if tag.lower() in video['tags'].lower():
            lt.addLast(filtered, video)
    
    return filtered

def filterByCategory(catalog, category):
    videosCatalog = mp.get(catalog['categories'], category)
    if videosCatalog:
        entry = me.getValue(videosCatalog)
        return entry["videos"]
    else:
        return lt.newList()

def filterByCountry(catalog, country):

    videosCountry = mp.get(catalog['countries'], country)
    if videosCountry:
        entry = me.getValue(videosCountry)
        return entry["videos"]
    else:
        return lt.newList()

def filterVideosByCountryAndCategory(catalog, category_id, country):
    """
    Retorna una sublista con los videos que cumplan el pais y la categoria
    """
    filteredVideos = lt.newList()

    videosCountry = mp.get(catalog["countries"], country)
    if videosCountry:
        entry = me.getValue(videosCountry)
        videos = lt.iterator(entry["videos"])
        for video in videos:
            if int(video["category_id"]) == category_id:
                lt.addLast(filteredVideos, video)

    return filteredVideos 

def getMostCommentedVideos(lista, num):
    if lt.size(lista) > 0:
        sortedVideos = se.sort(lista, cmpVideosByComments)
        defVideos = lt.newList()

        for counter in range(1, min(num, lt.size(sortedVideos))+1):

            video = lt.getElement(sortedVideos, counter)
            lt.addLast(defVideos, video)
        
        return defVideos
    
    else:
        return None

def getMostTrendingVideo(lista_videos):
    #print("**1*", lista_videos)
    videos_ordenados = se.sort(lista_videos, cmpVideosByTrendDate)
    #print("**2*", videos_ordenados)
    video_mas_trending = lt.firstElement(videos_ordenados)
    
    return video_mas_trending, getDeltaDays(video_mas_trending)

def getBestVideos(catalog, number, category_id, country):
    """
    Retorna los mejores videos
    """
    videos = filterVideosByCountryAndCategory(catalog, category_id, country)


    if lt.size(videos) > 0:
        sortedVideos = se.sort(videos, cmpVideosByLikes)
        defVideos = lt.newList()
        for counter in range(1, min(number, lt.size(sortedVideos))+1):

            video = lt.getElement(sortedVideos, counter)
            lt.addLast(defVideos, video)
        
        return defVideos
    
    else:
        return None

def videosSize(catalog):
    """
    Número de videos en el catalogo
    """
    return lt.size(catalog['videos'])


def categoriesSize(catalog):
    """
    Numero de categorias en el catalogo
    """
    return mp.size(catalog['categories'])

def getDeltaDays(video):
    videoTrendingDate = video["trending_date"]
    videoTrendingDate = datetime.strptime(videoTrendingDate, '%y.%d.%m')

    videoPublishDate = video["publish_time"]
    videoPublishDate = videoPublishDate.split("T")[0]
    videoPublishDate = datetime.strptime(videoPublishDate, '%Y-%m-%d')

    videoDeltaDays = videoTrendingDate - videoPublishDate

    return videoDeltaDays

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByComments(video1, video2):

    return (int(video1['comment_count']) > int(video2['comment_count']))

def compareMapVideoIds(id, entry):
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareCategories(cat1, cat2):
    if (int(cat1) == int(cat2)):
        return 0
    elif (int(cat1) > int(cat2)):
        return 1
    else:
        return 0

def compareMapCategoryIds(id, category):
    catentry = me.getKey(category)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return 0

def compareVideosIds(id1, id2):
    """
    Compara dos ids de dos videos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareCountriesByName(keyname, country):
    couentry = me.getKey(country)
    if (keyname == couentry):
        return 0
    elif (keyname > couentry):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return (int(video1['likes']) > int(video2['likes']))


def cmpVideosByTrendDate(video1, video2):
    video1DeltaDays = getDeltaDays(video1)
    video2DeltaDays = getDeltaDays(video2)

    return video1DeltaDays > video2DeltaDays