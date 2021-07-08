from flask import Flask, jsonify, render_template, request
from werkzeug.utils import redirect
from custom_modules.api_functions import get_car_by_plate, get_random_cars, get_brands_list

app = Flask(__name__)

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_car')
def show_car():
    car = get_car_by_plate("TB275F")
    
    return render_template('show_car.html', car=car)


@app.route('/random_car', methods=['GET', 'POST'])
def random_car():
    brands_list = get_brands_list()
    if request.method == 'POST':
        brand = request.form.get('brand').upper()
        car_list = get_random_cars(brand)
        return render_template('random_auto_tabel.html', car_list=car_list, brand=brand, brands_list=brands_list)
    else:
        return render_template('random_auto_tabel.html', brands_list=brands_list)

#
if __name__ == '__main__':
    app.run()