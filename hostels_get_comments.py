import time
import pandas as pd
import agoda
import booking
import google
import hostelworld
dt_info = time.strftime("%d-%m-%Y_%H.%M.%S", time.localtime())

# установка зависимостей: pip install requests pandas openpyxl bs4

# name_hostel - имя отеля, задается пользователем поля agoda_header, agoda_payload, google_url заполняются из вкладки
# network браузера (подставлять только указанные). 

# agoda_header и agoda_payload - данные из запроса 'HotelReviews'.

# pagename_booking - имя отеля (bodega-khao-san-party-hostel) из url (
# https://www.booking.com/hotel/th/bodega-khao-san-party-hostel.ru.html#tab-reviews) 

# google_url - строка Request URL запроса 'listentitiesreviews?aut...'.

# hostelworld_id_hostel - код отеля (315329) из url (
# https://www.hostelworld.com/st/hostels/p/315329/slumber-party-khao-san/). 

# формат: hostels = [{...},{...} ... {...},{...}]
hostels = [
    {
        'name_hostel': 'bodega-khao-san-party-hostel',
        'agoda_header': {
            "content-type": "application/json; charset=UTF-8",
            "Referer": "https://www.agoda.com/bodega-khao-san-party-hostel/hotel/bangkok-th.html?cid=-295"
        },
        'agoda_payload': "{\"hotelId\":35361027,\"hotelProviderId\":332,\"demographicId\":0,\"pageNo\":1,"
                         "\"pageSize\":20,\"sorting\":7,\"reviewProviderIds\":[332,3038,27901,28999,29100,27999,"
                         "27980,27989,29014],\"isReviewPage\":false,\"isCrawlablePage\":true,\"paginationSize\":5}",
        'pagename_booking': 'bodega-khao-san-party-hostel',
        'google_url': "https://www.google.ru/maps/preview/review/listentitiesreviews?authuser=0&hl=ru&gl=ru&pb=!1m2"
                      "!1y3522546374667733309!2y12592623997567025065!2m1!2i10!3e1!4m6!3b1!4b1!5b1!6b1!7b1!20b0!5m2"
                      "!1swKToY9OUGOaQ9u8PrLqegAY!7e81",
        'hostelworld_id_hostel': 315329
    }
]


def Reviews_to_excel(hostel):
    agoda_dict = agoda.GetReviews(hostel['agoda_header'], hostel['agoda_payload'], dt_info)
    booking_dict = booking.GetReviews(hostel['pagename_booking'], dt_info)
    google_dict = google.GetReviews(hostel['google_url'], dt_info)
    hw_dict = hostelworld.GetReviews(hostel['hostelworld_id_hostel'], dt_info)
    print("Collecting...")
    agoda_df = pd.DataFrame(agoda_dict, columns=['id', 'nickname', 'date', 'notes'])
    booking_df = pd.DataFrame(booking_dict, columns=['id', 'nickname', 'date', 'notes'])
    google_df = pd.DataFrame(google_dict, columns=['id', 'nickname', 'date', 'notes'])
    hostelworld_df = pd.DataFrame(hw_dict, columns=['id', 'nickname', 'date', 'notes'])
    print("Saving to excel file...")
    with pd.ExcelWriter(f"{hostel['name_hostel']}_reviews_dated_{dt_info}.xlsx") as writer:
        agoda_df.to_excel(writer, sheet_name="agoda", index=False)
        booking_df.to_excel(writer, sheet_name="booking", index=False)
        google_df.to_excel(writer, sheet_name="google", index=False)
        hostelworld_df.to_excel(writer, sheet_name="hostelworld", index=False)
    print("Done.")


if __name__ == '__main__':
    print("Start bypassing hostels.")
    for hsl in hostels:
        print(f"Going to hostel {hsl['name_hostel']}.")
        Reviews_to_excel(hsl)
        print(f"{hsl['name_hostel']} verified.")
    print("Reviews about all hostels collected!")
