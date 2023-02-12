import requests
import json
import os


def GetReviews(header, payload, dt_info):
    reviews_json_data = []
    print("Started reading site Agoda.")
    resp = requests.post("https://www.agoda.com/api/cronos/property/review/HotelReviews", data=payload, headers=header)
    if resp.status_code == 200:
        reviews_json_data = resp.json()
        print("Reading complete.")
        if os.path.isdir('raw_data'):
            print("Start saving data.")
            with open(f"raw_data/Agoda_raw_data_reviews_dated_{dt_info}.json", 'w') as outfile:
                json.dump(reviews_json_data, outfile)
            print("Saved.")
        else:
            print("Warning. Not found folder 'raw_data'. If you need raw data then create this folder.")
        print("Starting data transformation.")
        df_dict = []
        for review in reviews_json_data['commentList']['comments']:
            df_dict.append(
                [review['hotelReviewId'], review['reviewerInfo']['displayMemberName'], review['formattedReviewDate'],
                 review['reviewTitle'] + " " + review['reviewComments']])
        print("Complete data transformation.")
        return df_dict
    else:
        print(f"Server Agoda error, code: {resp.status_code}")
        return []
