import requests
from bs4 import BeautifulSoup
import os

usr_a = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'

def GetReviews(pagename, dt_info):
    print("Started reading site booking.")
    sess = requests.Session()
    sess.headers.update({'User-Agent': usr_a})
    all_rew = []
    page = 0
    while 1:
        print(f"Reading page #{page + 1}...")
        resp = sess.get(
            f"https://www.booking.com/reviewlist.ru.html?cc1=th&dist=1&pagename={pagename}&type=total&offset={page * 25};rows=25")
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, features="html.parser")
            rew_block = soup.find_all('li', class_='review_list_new_item_block')
            if len(rew_block) != 0:
                all_rew.extend(rew_block)
                page += 1
            else:
                break
        else:
            print(f"Server booking error, code: {resp.status_code}")
            return []
    print("Reading complete.")
    if os.path.isdir('raw_data'):
        print("Start saving data.")
        with open(f"raw_data/booking_raw_data_reviews_dated_{dt_info}.html", 'w', encoding='utf-8') as outfile:
            for rew_item in all_rew:
                outfile.write(rew_item.text)
        print("Saved.")
    else:
        print("Warning. Not found folder 'raw_data'. If you need raw data then create this folder.")
    print("Starting data transformation.")
    df_dict = []
    for review in all_rew:
        r_id = review.attrs['data-review-url']
        r_name = review.find('span', class_='bui-avatar-block__title').text
        r_date = review.find('div', class_='bui-grid__column-9 c-review-block__right').find('span', class_='c-review-block__date').text
        r_date = r_date[r_date.find(":") + 2:].rstrip()  # удаляем лишнее
        r_notes = review.find('span', class_='c-review__body').text
        r_notes = r_notes.replace("\n", " ")
        df_dict.append([r_id, r_name, r_date, r_notes])
    print("Complete data transformation.")
    return df_dict
