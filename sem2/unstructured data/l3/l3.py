import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

from typing import List
import requests
from geotext import GeoText
import matplotlib.pyplot as plt
import numpy as np
import gmplot


def list_of_visited_cities():
    # url = 'http://www.gutenberg.org/files/103/103-h/103-h.htm'
    # page = urllib.request.urlopen(url)
    # soup = BeautifulSoup(page, 'html.parser')
    text = open('pg103.txt', 'r').read()
    return [*set(GeoText(text).cities)]


def path_with_cities_from_csv(visited_cities):
    data = pd.read_csv('simplemaps-worldcities-basic.csv')
    cities_data = pd.DataFrame(data, columns=['city', 'lat', 'lng']).as_matrix()
    return sorted([(lat, lng) for city, lat, lng in cities_data if city in visited_cities],
                  key=lambda x: (x[1]))  # sort by longtitude


def visited_cities_lat_lng(cities):
    visited_cities = [0] * len(cities)
    i = 0
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    while i < len(cities):
        city = cities[i]
        r = requests.get(url, {'address': city, 'sensor': 'false'})
        if r.json()['status'] == 'OK':
            location = r.json()['results'][0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            visited_cities[i] = (city, lat, lng)
            i += 1
    return visited_cities


def path_with_cities_from_googleapi(cities):
    path_lat = np.ndarray([len(cities)])
    path_lng = np.ndarray([len(cities)])

    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    i = 0
    while i < len(cities):
        city = cities[i]
        r = requests.get(url, {'address': city})
        # if len(res) > 0:
        if r.json()['status'] == 'OK':
            location = r.json()['results'][0]['geometry']['location']
            path_lat[i] = location['lat']
            path_lng[i] = location['lng']
            i += 1
    return sorted([*zip(path_lat, path_lng)], key=lambda x: (x[1]))  # sort by longtitude


def distance(p1, p2):
    return abs(p1 - p2)


def correct_path(path):
    indices_to_remove = []
    for i in range(len(path) - 2):
        lat1, lng1 = path[i]
        lat2, lng2 = path[i + 1]
        lat3, lng3 = path[i + 2]
        # if distance(lng1, lng2) < 50 and distance(lat1, lat2) > 20:
        #     indices_to_remove.append(i + 1)
        if distance(lat1, lat3) < 30 and (distance(lat1, lat2) > 30 or distance(lat2, lat3) > 30):
            indices_to_remove.append(i + 1)
    print(len(indices_to_remove))
    for i in reversed(indices_to_remove):
        del path[i]
    return path


def draw_map(path, name='mymap'):
    """takes a list of tuples with (lat,lng) and file name for the result;
    draws path on map from given points; the points should be in appropriate order """
    path_lat, path_lng = zip(*path)

    gmap = gmplot.GoogleMapPlotter(25., 15., 3)
    gmap.plot(path_lat, path_lng, 'cornflowerblue', edge_width=5)
    gmap.plot((path_lat[0], path_lat[-1]), (path_lng[0], path_lng[-1]), 'cornflowerblue', edge_width=5)
    gmap.draw(name + '.html')


if __name__ == '__main__':
    cities = list_of_visited_cities()
    # cities = ['Laramie', 'Iowa City', 'Formosa', 'New York', 'Calais']

    # CITIES FROM CSV
    path = path_with_cities_from_csv(cities)
    draw_map(path, 'around_the_world_csv')
    draw_map(correct_path(path), 'around_the_world_csv_corrected')

    # CITIES FROM GOOGLEAPI
    path = path_with_cities_from_googleapi(cities)
    draw_map(path, 'around_the_world_google')
    draw_map(correct_path(path), 'around_the_world_google_corrected')
