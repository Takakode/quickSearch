'''
This is a simple script to search nearby place with google map.
Be careful about the price of use... there 200USD free use of Google map.
'''
from google_key import google_key
import googlemaps
import csv, time
from datetime import datetime

def search_places(gmaps, location, radius, language, type):
    results = []
    gmaps_results = gmaps.places_nearby(
                location=location,
                radius=radius,
                language=language,
                type=type
            )

    limit = 30
    count = 0
    while 'next_page_token' in gmaps_results :
        if count >= limit:
            print('limit exceed')
            exit()
        count = count + 1
        results.extend(gmaps_results['results'])
        try:
            time.sleep(2) # fix for page token
            gmaps_results = gmaps.places_nearby(
                location=(35.6382051,139.6935731),
                radius=50000,
                language=language,
                type='restaurant',
                page_token=gmaps_results['next_page_token']
                )
        except googlemaps.exceptions.ApiError as error:
            print(error)
            exit()
    print('Number of results for '+ type +' : ' + str(len(results)))
    return results


def write_results(
        results,
        file_name='results/search.csv',
        fieldnames=['name','place_id','business_status','rating','user_ratings_total', 'vicinity']
        ):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

if __name__ == '__main__':
    language = 'en-US'

    #location coordinate you can find on google map
    location=(35.6382051,139.6935731)

    # radius in meter
    radius=50000

    # To use the script you need your own key
    gmaps = googlemaps.Client(key=google_key)

    # You can check the type list here:  https://developers.google.com/maps/documentation/places/web-service/supported_types?hl=fr
    types = ['cafe', 'convenience_store']
    results = []
    for type in types:
        results.extend(
            search_places(
                gmaps=gmaps,
                location=location,
                radius=radius,
                language=language,
                type=type
                )
            )
    write_results(results)
