import requests
import json
import os


def GetReviews(url, dt_info):
    reviews_json_data = []
    print("Started reading site google.")
    resp = requests.get(url)
    if resp.status_code == 200:
        rt = resp.text[resp.text.find("\n") + 1:]
        reviews_json_data = json.loads(rt)
        print("Reading complete.")
        if os.path.isdir('raw_data'):
            print("Start saving data.")
            with open(f"raw_data/google_raw_data_reviews_dated_{dt_info}.json", 'w') as outfile:
                json.dump(reviews_json_data, outfile)
            print("Saved.")
        else:
            print("Warning. Not found folder 'raw_data'. If you need raw data then create this folder.")
        print("Starting data transformation.")
        df_dict = []
        for review in reviews_json_data[2]:
            df_dict.append([review[6], review[0][1], review[1], review[3]])
        print("Complete data transformation.")
        return df_dict
    else:
        print(f"Server google error, code: {resp.status_code}")
        return []
