# Endomondo activity areas
# Collecting tweets published via Endomondo. Visualizing the activity areas on a map.
# www.endomondo-activity-areas.com

import json
import re
import gmplot
import matplotlib.pyplot as plt
import numpy as np
import tweepy
from unidecode import unidecode
from pprint import pprint

# https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/

# Twitter account data
consumer_key = '---'
consumer_secret = '---'

# Generate application data within your Twitter account
access_token = '---'
access_token_secret = '---'


def search(api, query, count, max_id):
    search_res = api.search(q=query, count=count, max_id=max_id)
    res = []
    id_list = []
    for i in search_res:
        try:
            # i.id, i.user.location, i.place, i.place.name, i.place.bounding_box.coordinates
            # if unidecode(i.place.country) == 'United States':
            res.append({'country': unidecode(i.place.country),
                        'city': unidecode(i.place.name),
                        'text': i.text,
                        'coordinates': i.place.bounding_box.coordinates})
            id_list.append(i.id)
        except AttributeError:
            pass

    m = min(id_list) if id_list else 1
    return res, str(m - 1)


def search_for_more_tweets(limit, filename):
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    query = '#Endomondo'
    # # find the first max_id
    search_res = api.search(q=query, count=1)
    max_id = search_res[0].id_str

    more_tweets = []

    while max_id != '0':
        res, max_id = search(api, query, 100, max_id)
        more_tweets += res
        print(len(more_tweets))
        if len(more_tweets) > limit:
            break

    with open(filename + '.json', 'w') as outfile:
        json.dump(more_tweets, outfile, ensure_ascii=False)


def find_duration(text):
    try:
        duration_format = re.compile('\d*h?:?\d+m:\d+s')
        duration_time = duration_format.findall(text)[0].split(':')  # ['39m', '21s']
        duration_time = [int(i[:-1]) for i in duration_time]  # [39,21]
        if len(duration_time) == 3:
            hours = duration_time[0] + 1. / 60 * (duration_time[1] + 1 / 60 * duration_time[2])
        elif len(duration_time) == 2:
            hours = 1. / 60 * (duration_time[0] + 1 / 60 * duration_time[1])
    except:
        hours = 0.
    return round(hours, 2)


def find_distance(text):
    try:
        distance_format = re.compile('(\d+.\d+) (km|miles)')
        distance, units = distance_format.findall(text)[0]  # [('6.58', 'km')][0]
        distance = float(distance)
        distance = distance if units == 'km' else 1.6 * distance
    except:
        distance = 0.
    return round(distance, 2)


def calc_coordinates(coord):
    A, B, C, D = coord
    return round(.5 * (A[0] + B[0]), 4), round(.5 * (A[1] + D[1]), 4)


def parse_tweets(data, activity_names, country=None):
    activity_format = re.compile('(' + '|'.join(activity_names) + ')')

    activity_data_city = {}
    activity_data_sport = {}

    for l in data:
        if country is None or l['country'] == country:
            text = l['text']
            matched = activity_format.findall(text)
            if matched:
                sport = matched[0]
                coord = calc_coordinates(l['coordinates'][0])
                distance = find_distance(text)
                duration = find_duration(text)

                # add to the dictionary with results for cities
                if l['city'] not in activity_data_city:
                    activity_data_city[l['city']] = {sport: {'distance': distance,
                                                             'duration': duration,
                                                             'people': 1}}
                else:
                    tmp_sport = activity_data_city[l['city']].get(sport, {'distance': 0.,
                                                                          'duration': 0.,
                                                                          'people': 0})
                    tmp_dict = {'distance': distance,
                                'duration': duration,
                                'people': 1}
                    activity_data_city[l['city']][sport] = {key: val + tmp_dict[key]
                                                            for key, val in tmp_sport.items()}
                # add to the dictionary with results for sports
                if sport in activity_data_sport:
                    activity_data_sport[sport].append({'coordinates': coord,
                                                       'distance': distance,
                                                       'duration': duration})
                else:
                    activity_data_sport[sport] = [{'coordinates': coord,
                                                   'distance': distance,
                                                   'duration': duration}]

    return activity_data_city, activity_data_sport


def draw_points_on_map(sport_dict, col, name='worldmap', legend=True, country=None):
    """takes lists of lat and lng and file name for the result; draws points on a map"""
    # TODO better map would be https://plot.ly/python/scatter-plots-on-maps/
    if legend:
        print('Legend:')
        pprint(list(zip(activity_names, col)))

    if country == 'Poland':
        gmap = gmplot.GoogleMapPlotter(51.9194, 19.1451, 7)
    elif country == 'United States':
        gmap = gmplot.GoogleMapPlotter(37.0902, -95.7129, 5)
    else:
        gmap = gmplot.GoogleMapPlotter(25., 15., 3)

    for sport, val in sport_dict.items():  # val = [{'coordinates': c, 'distance': x, 'duration': t}, {}, ...]
        for d in val:
            c2, c1 = d['coordinates']
            color = col[activity_names.index(sport)]
            size = d['duration'] * 10
            gmap.scatter([c1], [c2], color=color)
    if country:
        gmap.draw(country.lower() + '.html')
    else:
        gmap.draw(name + '.html')


def pie_plots_per_city(cities, adata_city, col, characteristic):
    legend = {'distance': ' km', 'duration': ' h', 'people': ' ppl'}
    f, axarr = plt.subplots(len(characteristic), len(cities))

    for i_c, c in enumerate(cities):
        labels = [sp for sp in adata_city[c]]
        colors = [col[activity_names.index(l)] for l in labels]

        for i_d, d in enumerate(characteristic):
            sizes = np.array([adata_city[c][sport][d]
                              for sport in adata_city[c]])
            axarr[i_d, i_c].pie(sizes, labels=labels, colors=colors,
                                autopct=lambda val: str(np.round(val / 100. * sizes.sum(), 2)) + legend[d],
                                shadow=False, startangle=140)
            axarr[i_d, i_c].set_title(c + ' (' + d + ')')
            axarr[i_d, i_c].axis('equal')
    plt.show()


def plot_pie_charts(data):
    adata_city, adata_sport = parse_tweets(data, activity_names)
    # # choose from cities that have at least 3 types of activities
    # res = []
    # for city, d in adata_city.items():
    #     if len(d) > 2:
    #         res.append([city, len(d)])
    # pprint(res)

    cities = ['Sao Paulo', 'Barcelona', 'Riga']
    characteristic = ['distance', 'duration', 'people']
    pie_plots_per_city(cities, adata_city, col, characteristic)


def save_activity_map(country=None):
    adata_city, adata_sport = parse_tweets(data, activity_names, country)
    draw_points_on_map(adata_sport, col, country=country)
    # pprint(adata_city)
    # pprint(adata_sport)


if __name__ == '__main__':
    # search_for_more_tweets(1000, filename='data1000')

    data = json.load(open('data1000.json', 'r'))

    activity_names = ['swimming', 'cycling', 'running', 'walking']
    col = ['blue', 'indianred', 'darkorange', 'forestgreen']

    save_activity_map('Poland')
    save_activity_map('United States')

    plot_pie_charts(data)
