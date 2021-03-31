from flask import Flask, request, redirect, url_for, jsonify
from flask import render_template
from forms import SignupForm, PostForm, LoginForm,VehicleForm, VehicleSearchForm
from flask_login import LoginManager, current_user, login_user,login_required, logout_user
from models import users, get_user, User
from werkzeug.urls import url_parse
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)
login_manager.login_view = "login"
posts = []
vehicles = []


@app.route("/")
def index():
    return render_template("index.html", vehicles=vehicles)


@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)


@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)#Aquí guarda en la lista
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)

@app.route("/admin/vehicle/", methods=['GET', 'POST'], defaults={'vehicle_id': None})
@app.route("/admin/vehicle/<int:vehicle_id>/", methods=['GET', 'POST'])
#@login_required
def Vehicle_form(vehicle_id):
    form = VehicleForm()
    if form.validate_on_submit():
        typeVehicle = form.typeVehicle.data
        placa = form.placa.data
        cc = form.cc.data
        foto = form.foto.data
        capacity = form.capacity.data
        times = form.times.data
        model = form.model.data
        door = form.door.data
        position = random.randrange(0, 101, 2)
        vehicle = {'typeVehicle': typeVehicle,'cc': cc, 'placa': placa, 'foto': foto,'capacity':capacity,'times':times,'model':model,'door':door,'position':position}
        vehicles.append(vehicle)#Aquí guarda en la lista
        print(vehicles)
        #return jsonify(vehicles)
        return redirect(url_for('index'))
    return render_template("admin/vehicle_form.html", form=form)

@app.route("/admin/VehicleSearch/", methods=['GET', 'POST'], defaults={'vehicle_id': None})
@app.route("/admin/VehicleSearch/<int:vehicle_id>/", methods=['GET', 'POST'])
#@login_required
def VehicleSearch_form(vehicle_id):
    Listvehicle = []
    form = VehicleSearchForm()
    if form.validate_on_submit():
        
        placa = form.placa.data
        cc = form.cc.data
        if(placa!=''):
            vehicle = list(e for e in vehicles if e['placa']  == placa)
            #return jsonify(vehicle)
            print(vehicle[0]['placa'])
            return render_template("admin/vehicle_view.html", vehicle = vehicle)
        elif(cc!=''):
            #Bucar todos los carros cuyas cedulas sean del mismo propietario
            for e in vehicles:
                if(e['cc']==cc):
                    Listvehicle.append(e)
            return jsonify(Listvehicle)


        #return jsonify(vehicles)
        #return redirect(url_for('admin/vehicleEntry', ))
    return render_template("admin/VehicleSearch.html", form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))