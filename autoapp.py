from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
from custom_modules.api_functions import get_car_by_plate, get_random_cars, get_brands_list

import pandas as pd

import sqlite3

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_car', methods=['GET', 'POST'])
def show_car():
    if request.method == 'POST':
        kenteken = request.form.get('kenteken').upper().replace(" ","")
        car = get_car_by_plate(kenteken)

        if car == None:
            flash(f"Informatie voor kenteken <b>{kenteken}</b> niet kunnen vinden", "alert alert-warning")
        else:
            flash(f"Informatie opgehaald voor {car['kenteken']}", "alert alert-success")
        return render_template('show_car.html', car=car)
    else:
        return render_template('show_car.html')


@app.route('/random_car', methods=['GET', 'POST'])
def random_car():
    # setup database connection
    con = sqlite3.connect('database.db')
    
    # create the merken_table if it does not exist yet
    cursor = con.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS merken_tabel
                   (merk text)
                   ''')
    
    con.commit()
    
    # fetch the merken for the dropdown menu, from the database
    qry = '''
          select merk
          from merken_tabel
          '''
          
    merken_df   = pd.read_sql(qry, con)
    brands_list = merken_df['merk'].tolist()
    
    # if not available in the database, use function
    if len(merken_df) == 0:
        brands_list = get_brands_list()
        export_merken_df = pd.DataFrame({'merk': brands_list})
        export_merken_df.to_sql('merken_tabel', con, if_exists='replace')
    
    if request.method == 'POST':
        brand = request.form.get('brand').upper()
        car_list = get_random_cars(brand)
        return render_template('random_auto_tabel.html', car_list=car_list, brand=brand, brands_list=brands_list)
    else:
        return render_template('random_auto_tabel.html', brands_list=brands_list)

#
if __name__ == '__main__':
    app.run()
    