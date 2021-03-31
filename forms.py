from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')

class VehicleForm(FlaskForm):
    typeVehicle = SelectField('Tipo de Vehiculo', choices=[(''),('carro'),('moto'),('bicicleta')])
    placa = StringField('Placa')
    cc = StringField('Cedula del propietario')
    foto = StringField('Foto')
    capacity = StringField('Cilindraje')
    times = StringField('Tiempos')   
    model = StringField('Modelo')
    door = StringField('Numero de puertas')
    #position = StringField('Numero de puertas')
        
    
    submit = SubmitField('Enviar')

class VehicleSearchForm(FlaskForm):
    placa = StringField('Placa')
    cc = StringField('cedula')
    
        
    
    submit = SubmitField('Enviar')

class VehicleEntryForm(FlaskForm):
    placa = StringField('Placa')
    cc = StringField('cedula')       
    
    submit = SubmitField('Enviar')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')