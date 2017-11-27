# Endomondo activity areas
# Collecting tweets published via Endomondo. Visualizing the activity areas on a map.
# www.endomondo-activity-areas.com
from pprint import pprint
import gmplot
import re
import numpy as np
import requests
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import json
from unidecode import unidecode
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Twitter account data
consumer_key = '---'
consumer_secret = '---'

# Generate application data within your Twitter account
access_token = '---'
access_token_secret = '---'


class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            with open('twitter.json', 'r') as f:
                # f.write(data)
                # print(data)
                # return True
                line = f.readline()
                tweet = json.loads(line)
                print(json.dumps(tweet, indent=4))
        except BaseException as e:
            print('Error on_data: %s' % str(e))
            time.sleep(5)
        return True

    def on_error(self, status_code):
        print(status_code)


def useStdOutListener(query='#Endomondo'):
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[query])


def search(api, query, count, max_id):
    search_res = api.search(q=query, count=count, max_id=max_id)
    res = []
    id_list = []
    for i in search_res:
        try:
            # print(i.id)
            # print(i) print(i.user) print(i.user.location) print(i.place) print(i.place.name) print(i.place.full_name)
            # print(i.place.name) res.append(i.place.name) print(i.place.bounding_box.coordinates)
            # res.append({'full_name': unidecode(i.place.full_name),
            #             'city': unidecode(i.place.name),
            #             'country': unidecode(i.place.country),
            #             'text': i.text,
            #             'coordinates': i.place.bounding_box.coordinates})
            #
            if unidecode(i.place.country) == 'United States':
                # if True:
                res.append({'country': unidecode(i.place.country),
                            'city': unidecode(i.place.name),
                            'text': i.text,
                            'coordinates': i.place.bounding_box.coordinates})
                id_list.append(i.id)
        except AttributeError:
            pass

    m = min(id_list) if id_list else 1
    return res, str(m - 1)


def search_for_more_tweets(limit):
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

    with open('data.json', 'w') as outfile:
        json.dump(more_tweets, outfile, ensure_ascii=False)
        # return more_tweets


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


def parse_results(tweets_data):
    # pprint(tweets_data)  # shows structure of data_dict
    activity_names = ['Climbing Stairs', 'Cross-Country Skiing', 'Cycling', 'Dancing', 'Fitness Walking', 'Hiking',
                      'Riding', 'Roller skating', 'Running', 'Skateboarding', 'Skiing', 'Swimming', 'Volleyball',
                      'Mountain biking', 'Walking']
    activity_names = map(lambda x: x.lower(), activity_names)
    activity_format = re.compile('(' + '|'.join(activity_names) + ')')

    activity_data = {}
    distance_format = re.compile('\d+.\d+ km')

    for country, country_val in tweets_data.items():
        for city, texts in country_val.items():
            for text in texts:
                match = activity_format.findall(text)
                if match:
                    found_activity = match[0]
                    try:
                        distance = float(
                            distance_format.findall(text)[0].split()[0])  # ['6.58 km'][0].split()[0] turn to float
                    except:
                        distance = 0.
                    try:
                        duration = find_duration(text)
                    except:
                        duration = 0.

                    # if found_activity in activity_data.keys():
                    #     if city in activity_data[found_activity].keys():
                    #         activity_data[found_activity][city]['distance'] += distance
                    #         activity_data[found_activity][city]['duration'] += duration
                    #     else:
                    #         activity_data[found_activity][city] = {'distance': distance, 'duration': duration}
                    # else:
                    #     activity_data[found_activity] = {city: {'distance': distance, 'duration': duration}}

                    key = city  # + ', ' + country
                    if key in activity_data:
                        if found_activity in activity_data[key]:
                            activity_data[key][found_activity]['distance'] += distance
                            activity_data[key][found_activity]['duration'] += duration
                        else:
                            activity_data[key][found_activity] = {'distance': distance, 'duration': duration}
                    else:
                        activity_data[key] = {found_activity: {'distance': distance, 'duration': duration}}

    pprint(len(activity_data.keys()))
    print(list(activity_data.keys())[0:10])
    lat, lng = find_lat_lng_google(list(activity_data.keys())[0:10])
    draw_points_on_map(lat, lng)


def parse_tweets(data, activity_names, country=None):
    tweets_per_city = {}

    for l in data:
        coord = calc_coordinates(l['coordinates'][0])
        if l['country'] not in tweets_per_city.keys():
            tweets_per_city[l['country']] = {l['city']: [(l['text'], coord)]}
        elif l['city'] not in tweets_per_city[l['country']].keys():
            tweets_per_city[l['country']][l['city']] = [(l['text'], coord)]
        else:
            tweets_per_city[l['country']][l['city']].append((l['text'], coord))
    # pprint(tweets_per_city)

    ##
    activity_format = re.compile('(' + '|'.join(activity_names) + ')')

    activity_data_for_city = {}
    activity_data_sport = {}

    for l in data:
        if country is not None:
            if l['country'] != country:
                break
        text = l['text']
        matched = activity_format.findall(text)
        if matched:
            sport = matched[0]
            coord = calc_coordinates(l['coordinates'][0])
            distance = find_distance(text)
            duration = find_duration(text)

            # add to the dictionary with results for cities
            if l['city'] not in activity_data_for_city:
                activity_data_for_city[l['city']] = {sport: {'distance': distance,
                                                             'duration': duration,
                                                             'people': 1}}
            else:
                tmp_sport = activity_data_for_city[l['city']].get(sport, {'distance': 0.,
                                                                          'duration': 0.,
                                                                          'people': 0})
                tmp_dict = {'distance': distance,
                            'duration': duration,
                            'people': 1}
                activity_data_for_city[l['city']][sport] = {key: val + tmp_dict[key]
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

    return activity_data_for_city, activity_data_sport


def find_lat_lng_google(cities):  # not used
    # Free up to 2,500 requests per day.
    lat = np.zeros(len(cities))
    lng = np.zeros(len(cities))
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    i = 0
    t = 0
    while i < len(cities):
        city = cities[i]
        r = requests.get(url, {'address': city})
        t += 1
        print(r.json())
        if r.json()['status'] == 'OK':
            location = r.json()['results'][0]['geometry']['location']
            lat[i] = location['lat']
            lng[i] = location['lng']
            i += 1
            t = 0

        if t > 3:  # if there were more than 3 requests with that city name
            i += 1
            t = 0
    return lat, lng


def draw_points_on_map(sport_dict, name='mymap'):
    """takes lists of lat and lng and file name for the result; draws points on a map"""
    gmap = gmplot.GoogleMapPlotter(25., 15., 3)
    # TODO for-loop for all sports (different colors)
    for sport, val in sport_dict.items():  # val = [{'coordinates': c, 'distance': x, 'duration': t}, {}, ...]
        for d in val:
            c2, c1 = d['coordinates']
            gmap.scatter([c1], [c2], col[activity_names.index(sport)], size=50)
            # gmap.scatter([c1], [c2], 'cornflowerblue', size=50)
            # gmap.scatter(lat, lng, 'cornflowerblue', size=50)
    gmap.draw(name + '.html')


def pie_plots_per_city(adata_city):
    pass


if __name__ == '__main__':
    # search_for_more_tweets(1000)
    data = json.load(open('data1000.json', 'r'))
    # activity_names = ['Climbing Stairs', 'Cross-Country Skiing', 'Cycling', 'Dancing', 'Fitness Walking', 'Hiking',
    #                   'Riding', 'Roller skating', 'Running', 'Skateboarding', 'Skiing', 'Swimming', 'Volleyball',
    #                   'Mountain biking', 'Walking']
    # activity_names = [*map(lambda x: x.lower(), activity_names)]
    activity_names = ['swimming', 'cycling', 'running', 'walking']

    #
    country = 'United States'
    adata_city, adata_sport = parse_tweets(data, activity_names, country)
    print('\n_______________________________________________________________________________________________\n')
    pprint(adata_city)
    print('\n_______________________________________________________________________________________________\n')
    pprint(adata_sport)

    # cmap = plt.get_cmap('viridis')
    # col = cmap(np.linspace(0, 1, len(activity_names)))
    # col = [colors.rgb2hex(c) for c in col]
    col = ['blue', 'indianred', 'darkorange', 'forestgreen']
    print('Legend:')
    pprint(dict(zip(activity_names, col)))

    # pie_plots_per_city(adata_city)
    draw_points_on_map(adata_sport)
