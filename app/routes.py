from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app.custom_modules.api_functions import get_car_by_plate, get_random_cars, get_brands_list
import pandas as pd
import sqlite3

from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm



###### routes
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is authenticated, open the homepage
    if current_user.is_authenticated:
        redirect(url_for('index'))
    # if the user it not authenticated, present the login form on the login.html template
    form = LoginForm()
    # if user succesfully logged in, get the user from the form data
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'alert alert-danger')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index')) 
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # get the data from the form
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
    
    
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'alert alert-success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route('/show_car', methods=['GET', 'POST'])
@login_required
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
@login_required
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succesfully logged out", "alert alert-info")
    return redirect(url_for('index'))

#
if __name__ == '__main__':
    app.run()
    