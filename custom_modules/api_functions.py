import requests

def get_car_by_plate(plate):
    resp = requests.get("https://opendata.rdw.nl/resource/m9d7-ebf2.json?kenteken=TB725F")
    resp_dict = resp.json()
    car  = resp_dict[0]
    return car
    
    
def get_random_cars(brand):
    url = f"https://opendata.rdw.nl/resource/m9d7-ebf2.json?merk={brand}"
    resp = requests.get(url)
    resp_list = resp.json()
    return resp_list
    