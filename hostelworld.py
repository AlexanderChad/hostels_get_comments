import requests
import json
import os


def GetReviews(id_hostel, dt_info):
    reviews_json_data = []
    print("Started reading site hostelworld.")
    page = 1
    while page:
        print(f"Reading page #{page}...")
        response = requests.get(
            f"https://api.m.hostelworld.com/2.2/properties/{id_hostel}/reviews/?sort=newest&allLanguages=true&page={page}&monthCount=36&application=web")
        if response.status_code == 200:
            page += 1
            reviews_json_data.extend(json.loads(response.text)['reviews'])
        elif response.status_code == 400:
            page = 0
        else:
            print(f"Server hostelworld error, code: {response.status_code}")
            return []
    print("Reading complete.")
    if os.path.isdir('raw_data'):
        print("Start saving data.")
        with open(f"raw_data/hostelworld_raw_data_reviews_dated_{dt_info}.json", 'w') as outfile:
            json.dump(reviews_json_data, outfile)
        print("Saved.")
    else:
        print("Warning. Not found folder 'raw_data'. If you need raw data then create this folder.")
    print("Starting data transformation.")
    df_dict = []
    for review in reviews_json_data:
        df_dict.append([review['id'], review['user']['nickname'], review['date'], review['notes']])
    print("Complete data transformation.")
    return df_dict
