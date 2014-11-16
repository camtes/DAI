## -*- coding: utf-8 -*-
##
## Autor: Carlos Campos Fuentes

import web
import anydbm
import re
from pymongo import MongoClient
from web import form
from web.contrib.template import render_mako

web.config.debug = False

urls = ('/', 'index',
		'/logout', 'logout',
		'/datos', 'datos',
		'/modifica-datos', 'modifica',
		'/pagina3', 'pagina3',
		'/pagina4', 'pagina4'
		)

app = web.application(urls, locals())

session = web.session.Session(app, web.session.DiskStore('sessions'))

templates = render_mako(
	directories=['templates'],
	input_encoding='utf-8',
	output_encoding='utf-8',
	)

# Formularios

formulario = form.Form(
	form.Textbox('nombre', form.notnull, maxlenght="30", description="Nombre: "),
	form.Textbox('apellidos', form.notnull, maxlenght="50", description="Apellidos: "),
	form.Textbox("dni", form.notnull, maxlenght="8", description="DNI: "),
	form.Textbox('correo', form.notnull,
		form.Validator("Formato de correo no valido", lambda i: email.match(i)),
		maxlenght="50", description="Correo electrónico: "),
	form.Textbox('visa', form.notnull,
		form.Validator("El formato de la VISA no es valido.", lambda i: visa.match(i)),
		maxlenght="19", description="VISA: "),
	form.Dropdown('dia', range(1,32), description="Día: "),
	form.Dropdown('mes', range(1,13), description="Mes: "),
	form.Dropdown('ano', range(1900, 2015), description="Año: "),
	form.Textarea("descripcion", maxlenght="120", description="Descripción: "),
	form.Password("contrasena", form.notnull,
		form.Validator("La contraseña debe de tener 8 caracteres como mínimo.", lambda i: len(str(i))>7),
		maxlenght="8", description="Contraseña: "),
	form.Password("contrasena2", form.notnull,
		form.Validator("La contraseña debe de tener 8 caracteres como mínimo.", lambda i: len(str(i))>7),
		maxlenght="8", description="Vuelve a introducir la contraseña: "),
	form.Radio("pago", ["PayPal", "Tarjeta"], form.notnull, description="Forma de pago: "),
	form.Checkbox('condiciones',
		form.Validator("Debes de aceptar las clausulas", lambda i: i == 'true'), value='true'),
	form.Button("Enviar"),

	validators = [
		form.Validator("Fecha incorrecta.", lambda x: not(
			(int(x.dia)==29 and int(x.mes)==2) or
			(int(x.dia)==29 and int(x.mes)==2 and int(x.anio)%4!=0) or
			(int(x.dia)==30 and int(x.mes)==2) or
			(int(x.dia)==31 and int(x.mes)%2==0)
		)),
		form.Validator("Las contraseñas no coinciden.", lambda i: i.contrasena == i.contrasena2),
	]
)


formLogin = form.Form(
	form.Textbox('username', form.notnull, maxlenght="30", description="Correo "),
	form.Password('passwd', maxlenght="15", description="Contraseña "),
	form.Button("Login")
	)


# Expresiones regulares
email = re.compile(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$')
visa = re.compile(r'[0-9]{4}([\ \-]?)[0-9]{4}([\ \-]?)[0-9]{4}([\ \-]?)[0-9]{4}([\ \-]?)')

# Variables y funciones
def insert_message(user):
	return str("Bienvenido " + str(user) + " (<a href='/logout'>Logout</a>)")

def insert_last():
	return str("\
			<ol>\
				<li> "+ str(session.primera) + "</li>\
				<li> "+ str(session.segunda) + "</li>\
				<li> "+ str(session.tercera) + "</li>\
			</ol> \
		")

def read_bd():
	data = {}
	conn = MongoClient('mongodb://localhost:27017/')
	db = conn.app.usuarios
	items = db.find_one()
	conn.close()

	return items


def insert_data():
	data = read_bd()

	# Creamos cadena de texto
	return str("\
		<ul>\
			<li> Nombre: "+ data["nombre"] +"</li>\
			<li> Apellidos: "+ data["apellidos"] +"</li>\
			<li> DNI: "+ data["dni"] +"</li>\
			<li> Correo: "+data["correo"] +"</li>\
			<li> VISA: "+ data["visa"] +"</li>\
			<li> Fecha de Nacimiento: "+ data["dia"] +"/"+ data["mes"] +"/"+ data["ano"] +"</li>\
			<li> Descripcion: "+ data["descripcion"] + "</li>\
		</ul> \
		<a href='/modifica-datos'>Modificar datos</a>\
		")

def insert_form_data():
	data = read_bd()

	formulario = form.Form(
		form.Textbox('nombre', [("value", "hola")], form.notnull, maxlenght="30", description="Nombre: ", value=str(data["nombre"])),
		form.Textbox('apellidos', form.notnull, maxlenght="50", description="Apellidos: ", value=str(data["apellidos"])),
		form.Textbox("dni", form.notnull, maxlenght="8", description="DNI: ", value=str(data["dni"])),
		form.Textbox('correo', form.notnull,
			form.Validator("Formato de correo no valido", lambda i: email.match(i)),
			maxlenght="50", description="Correo electrónico: ", value=str(data["correo"])),
		form.Textbox('visa', form.notnull,
			form.Validator("El formato de la VISA no es valido.", lambda i: visa.match(i)),
			maxlenght="19", description="VISA: ", value=str(data["visa"])),
		form.Dropdown('dia', range(1,32), description="Día: ", value=int(data["dia"])),
		form.Dropdown('mes', range(1,13), description="Mes: ", value=int(data["mes"])),
		form.Dropdown('ano', range(1900, 2015), description="Año: ", value=int(data["ano"])),
		form.Textarea("descripcion", maxlenght="120", description="Descripción: ", value=str(data["descripcion"])),
		form.Password("contrasena",
			form.Validator("La contraseña debe de tener 8 caracteres como mínimo.", lambda i: len(str(i))>7),
			maxlenght="8", description="Contraseña: "),
		form.Password("contrasena2",
			form.Validator("La contraseña debe de tener 8 caracteres como mínimo.", lambda i: len(str(i))>7),
			maxlenght="8", description="Vuelve a introducir la contraseña: "),
		form.Radio("pago", ["PayPal", "Tarjeta"], form.notnull, description="Forma de pago: ", checked=str(data["pago"])),
		form.Checkbox('condiciones',
			form.Validator("Debes de aceptar las clausulas", lambda i: i == 'true'), value='true'),
		form.Button("Enviar"),

		validators = [
			form.Validator("Fecha incorrecta.", lambda x: not(
				(int(x.dia)==29 and int(x.mes)==2) or
				(int(x.dia)==29 and int(x.mes)==2 and int(x.anio)%4!=0) or
				(int(x.dia)==30 and int(x.mes)==2) or
				(int(x.dia)==31 and int(x.mes)%2==0)
			)),
			form.Validator("Las contraseñas no coinciden.", lambda i: i.contrasena == i.contrasena2),
		]
	)

	return formulario

class index:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			formRegistro = formulario()
			return templates.template(titulo = "Inicio", form = form, formR = formRegistro)
		else:
			return templates.template(titulo = "Inicio", message = insert_message(session.user), ultimas = insert_last())

	def POST(self):
		form = formLogin()
		formR = formulario()

		# Formulario de registro
		if formR.validates():
			conn = MongoClient('mongodb://localhost:27017')
			db = conn.app.usuarios

			# Añado entrada a la bd
			aux = web.input()

			db_usuarios = {
				"nombre": aux.nombre,
				"apellidos": aux.apellidos,
				"dni": aux.dni,
				"correo": aux.correo,
				"visa": aux.visa,
				"dia": aux.dia,
				"mes": aux.mes,
				"ano": aux.ano,
				"descripcion": aux.descripcion,
				"contrasena": aux.contrasena,
				"contrasena2": aux.contrasena2,
				"pago": aux.pago,
			}

			db.insert(db_usuarios)

			items = db.find_one()

			#Cerramos la conexión
			conn.close()

			print items
			raise web.seeother('/')

		# Formulario de login
		if form.validates():
			aux = web.input()

			#Comprobamos el usuario y contraseña
			conn = MongoClient('mongodb://127.0.0.1:27017')
			db = conn.app.usuarios
			usuario = db.find_one({"correo": aux.username})

			if (usuario["contrasena"] == aux.passwd):
				session.user = usuario["nombre"]
				session.primera = " "
				session.segunda = " "
				session.tercera = " "
				return templates.template(titulo = "Inicio",
					message = insert_message(session.user), ultimas = insert_last())
			else:
				return templates.template(titulo = "Inicio", form = form, formR = formR)

		if not form.validates() or formR.validates():
			return templates.template(titulo = "Inicio", form = form, formR = formR)

class datos:
	def GET(self):
		session.tercera = session.segunda
		session.segunda = session.primera
		session.primera = "<a href='datos'>Datos</a>"
		return templates.template(titulo = "Datos",
			message = insert_message(session.user), content = insert_data(), ultimas = insert_last())


class modifica:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Modificar datos", form = form)
		else:
			form = insert_form_data()
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='modifica-datos'>Modificar datos</a>"
			return templates.template(titulo = "Modificar datos",
				message = insert_message(session.user),
				ultimas = insert_last(),
				formEdit = form().render())

	def POST(self):
		form = formulario()
		if not form.validates():
			raise web.seeother('/modifica-datos')
		else:
			aux = web.input()
			conn = MongoClient('mongodb://localhost:27017')
			db = conn.app.usuarios

			last_item = db.find_one()
			last_id = last_item["_id"]

			# Grabo los datos en la base de datos
			if aux.contrasena != "":
				db_usuarios = {
					"nombre": str(aux.nombre),
					"apellidos": str(aux.apellidos),
					"dni": str(aux.dni),
					"correo": str(aux.correo),
					"visa": str(aux.visa),
					"dia": str(aux.dia),
					"mes": str(aux.mes),
					"ano": str(aux.ano),
					"descripcion": str(aux.descripcion),
					"contrasena": str(aux.contrasena),
					"contrasena2": str(aux.contrasena2),
					"pago": str(aux.pago),
				}
			else:
				db_usuarios = {
					"nombre": str(aux.nombre),
					"apellidos": str(aux.apellidos),
					"dni": str(aux.dni),
					"correo": str(aux.correo),
					"visa": str(aux.visa),
					"dia": str(aux.dia),
					"mes": str(aux.mes),
					"ano": str(aux.ano),
					"descripcion": str(aux.descripcion),
					"contrasena": str(last_item["contrasena"]),
					"contrasena2": str(last_item["contrasena2"]),
					"pago": str(aux.pago),
				}

			db.update({"_id":last_id},db_usuarios)

			# Cerramos la base de datos
			conn.close()

			raise web.seeother('/datos')


class pagina3:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 3", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina3'>Pagina 3</a>"
			return templates.template(titulo = "Pagina 3",
				message = insert_message(session.user), ultimas = insert_last())

class pagina4:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 4", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina4'>Pagina 4</a>"
			return templates.template(titulo = "Pagina 4",
				message = insert_message(session.user), ultimas = insert_last())

class logout:
	def GET(self):
		session.kill()
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()
