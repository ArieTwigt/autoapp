from flask import Flask, jsonify, render_template
from werkzeug.utils import redirect
from custom_modules.api_functions import get_car_by_plate, get_random_cars

app = Flask(__name__)

# routes
@app.route('/')
def index():
    redirect
    return "Hello world"

@app.route('/show_car')
def show_car():
    car = get_car_by_plate("TB275F")
    
    return jsonify(car)


@app.route('/random_car')
def random_car():
    brand = "AUDI" # <TODO> get from user input
    car_list = get_random_cars(brand)
    return render_template('random_auto_tabel.html', car_list=car_list)


#
if __name__ == '__main__':
    app.run()