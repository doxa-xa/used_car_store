from main import app, db, render_template, request, flash, redirect, url_for, login_manager, login_user, logout_user, login_required, current_user, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, secure_filename
from models import User, bcrypt, Car, CarPhoto
from utils import strToBool
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST' and request.form.get('username'):
        if 'username' and 'passwd' in request.form.keys():
            username = request.form.get('username')
            passwd = request.form.get('passwd')
            user = User.query.filter_by(email=username).first()
            if user and bcrypt.check_password_hash(user.password_hash, passwd):
                login_user(user)
                return render_template('main.html',user=user)
            else:
                flash('Username or password are incorrect')
                return redirect(url_for('login'))
    else:
        return render_template('front.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        keys = request.form.keys()
        
        if all(key in keys for key in ('fname',
                                       'sname',
                                       'email',
                                       'passwd')):
            passwd = bcrypt.generate_password_hash(password=request.form.get('passwd'))
            user = User(name=request.form.get('fname'),
                        surname=request.form.get('sname'),
                        email=request.form.get('email'),
                        password_hash=passwd)
            db.session.add(user)
            db.session.commit()
            flash(f'User {request.form.get("fname")} {request.form.get("sname")} has beed created')
            return redirect(url_for('login'))
        else:
            flash('Please fill all the fields')
            return redirect(url_for('login'))
    else:
        return render_template('register.html')
    
@login_required
@app.route('/addcar',methods=['GET','POST'])
def add_car():
    if request.method == 'POST':
        form = request.form
        if all(key in form.keys() for key in ('price','brand','model','year','milage','fuel')):
            car = Car(
                customer_id=current_user.id,
                price=float(form.get('price')),
                brand=form.get('brand'),
                model=form.get('model'),
                manufactured=int(form.get('year')),
                milage=int(form.get('milage')),
                fuel=form.get('fuel'),
                power=int(form.get('power')),
                engine=float(form.get('vol')),
                doors=int(form.get('doors')),
                steering=form.get('wheel'),
                gearbox=form.get('gear'),
                ac=strToBool(form.get('ac')),
                info=form.get('info'),
                stereo=strToBool(form.get('stereo')),
                satnav=strToBool(form.get('navi')),
                awd=strToBool(form.get('awd')),
                abs=strToBool(form.get('abs')),
                esp=strToBool(form.get('esp')),
                cruize_control=strToBool(form.get('cruise')),
                electric_windows=strToBool(form.get('elwindows')),
                airbag=strToBool(form.get('airbag')),
                alloy_wheels=strToBool(form.get('alloywheels')),
                central_locking=strToBool(form.get('clock'))
            )
            db.session.add(car)
            db.session.commit()
        else:
            flash('Please fill all mandatory fields')
            return redirect(url_for('upload_photos'))
    return render_template('addcar.html', user=current_user)

@login_required
@app.route('/photos',methods=['GET','POST'])
def upload_photos():
    if request.method == 'POST':
        if 'photos' not in request.files:
            flash('file is empty or corrupted')
            return redirect(url_for('upload_photos'))
        file = request.files['photos']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('upload_photos'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = f'static/photos/{file.filename}'
            photo = CarPhoto(
                car_id = request.form.get('carid'),
                photo_url = filepath
            )
            db.session.add(photo)
            db.session.commit()
            file.save(filepath)
            flash('photos uploaded')
            return redirect(url_for('add_car'))
    else:
        cars = Car.query.filter_by(customer_id=current_user.id).all()
        return render_template('addphotos.html',user=current_user,cars=cars)


@login_required
@app.route('/removeycar')
def remove_car():
    return render_template('removecar.html', user=current_user)

@login_required
@app.route('/modifycar')
def modify_car():
    return render_template('modifycar.html', user=current_user)

@login_required    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_required
@app.route('/editprofile', methods=['GET','POST'])
def edit_profile():
    if request.method == 'POST':
        if 'phone' and 'address' in request.form.keys():
            user = User.query.filter_by(id=current_user.id).first()
            user.phone = request.form.get('phone')
            user.address = request.form.get('address')
            db.session.add(user)
            db.session.commit()
            flash('your profile has been updated')
            return redirect(url_for('edit_profile'))
        elif 'file' not in request.files:
            flash('file is empty or corrupted')
            return redirect(url_for('edit_profile'))
        file = request.files['file']
        if file.filename == '':
            print(file.filename)
            flash('No file selected')
            return redirect(url_for('edit_profile'))
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = f'static/{file.filename}'
            user = User.query.filter_by(id=current_user.id).first()
            user.profile_pic_url = filepath
            db.session.add(user)
            db.session.commit()
            print(filepath, filename)
            file.save(filepath)
            flash('photos uploaded')
            return redirect(url_for('add_car'))
    else:        
        return render_template('editprofile.html', user=current_user)

@login_required
@app.route('/listcars')
def list_cars():
    cars = Car.query.all()
    car_photos = CarPhoto.query.all()
    return render_template('listcars.html', user=current_user,cars=cars, photos=car_photos)

@login_required
@app.route('/view/<car_id>')
def view_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    photos = CarPhoto.query.filter_by(car_id=car_id)
    return render_template('viewcar.html', user=current_user, car=car, photos=photos)


@login_required
@app.route('/main')
def main_portal():
    return render_template('main.html',user=current_user)