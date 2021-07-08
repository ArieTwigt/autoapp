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
    
    
def get_brands_list():
    url = "https://opendata.rdw.nl/resource/m9d7-ebf2.json?$query=SELECT DISTINCT(merk) WHERE voertuigsoort = 'Personenauto'"
    resp = requests.get(url)
    brands_dict = resp.json()
    brands_list = [list(brand.values())[0] for brand in brands_dict ]
    return brands_list